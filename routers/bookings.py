# routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from auth import get_current_user, require_admin

router = APIRouter(prefix="/bookings", tags=["bookings"])


# ── GUEST: ver habitaciones disponibles por fechas ──────────────────
@router.get("/available")
def get_available_rooms(
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # busca room_ids con reservas confirmadas que solapen con las fechas
    occupied = db.query(models.Booking.room_id).filter(
        models.Booking.status == "confirmed",
        models.Booking.check_in < check_out,
        models.Booking.check_out > check_in
    )
    # devuelve habitaciones activas que NO están en la lista ocupada
    return db.query(models.Room).filter(
        models.Room.is_active == True,
        ~models.Room.id.in_(occupied)
    ).all()


# ── GUEST: ver mis reservas ─────────────────────────────────────────
@router.get("/mine", response_model=list[schemas.BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # filtra solo las reservas del usuario autenticado
    return db.query(models.Booking).filter(
        models.Booking.user_id == current_user.id
    ).all()


# ── ADMIN: ver TODAS las reservas ───────────────────────────────────
@router.get("/", response_model=list[schemas.BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)  # solo admin puede ver todas
):
    return db.query(models.Booking).all()


# ── ADMIN: ver check-ins de hoy ─────────────────────────────────────
@router.get("/today", response_model=list[schemas.BookingResponse])
def get_today_checkins(
    db: Session = Depends(get_db),
    admin_id: int = Depends(require_admin)
):
    # filtra reservas cuyo check_in es hoy
    return db.query(models.Booking).filter(
        models.Booking.check_in == date.today(),
        models.Booking.status == "confirmed"
    ).all()


# ── GUEST/ADMIN: crear reserva ──────────────────────────────────────
@router.post("/", response_model=schemas.BookingResponse, status_code=201)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Regla 1: check_out debe ser después de check_in
    if booking.check_in >= booking.check_out:
        raise HTTPException(
            status_code=400,
            detail="Check-out must be after check-in"
        )

    # Regla 2: no reservas en el pasado
    if booking.check_in < date.today():
        raise HTTPException(
            status_code=400,
            detail="Check-in cannot be in the past"
        )

    # Regla 3: la habitación existe y está activa
    db_room = db.query(models.Room).filter(
        models.Room.id == booking.room_id
    ).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not db_room.is_active:
        raise HTTPException(status_code=400, detail="Room is not available")

    # Regla 4: no solapamiento con reservas existentes
    overlapping = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.status == "confirmed",
        models.Booking.check_in < booking.check_out,
        models.Booking.check_out > booking.check_in
    ).first()
    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Room already booked for these dates"
        )

    # calcular precio total automáticamente
    nights = (booking.check_out - booking.check_in).days
    total_price = nights * db_room.price

    # crear la reserva
    new_booking = models.Booking(
        user_id=current_user.id,  # viene del JWT, no del body
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status="confirmed",        # siempre empieza confirmada
        total_price=total_price    # calculado automáticamente
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# ── GUEST/ADMIN: cancelar reserva ──────────────────────────────────
@router.put("/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # solo el titular o un admin puede cancelar
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to cancel this booking"
        )

    # no cancelar reservas ya pasadas
    if booking.check_in < date.today():
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel a past booking"
        )

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking


# ── GUEST/ADMIN: ver una reserva por id ────────────────────────────
@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # guest solo puede ver sus propias reservas
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view this booking"
        )
    return booking