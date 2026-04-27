from fastapi import APIRouter, Depends, HTTPException # Added APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import oauth2_scheme , get_current_user


# 1. Create the router object
router = APIRouter(prefix="/bookings", tags=["bookings"])

# 2. Add the decorator @router.get
@router.get("/available")
def get_available_rooms(
    check_in: str,
    check_out: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    # Find IDs of rooms that have overlapping bookings
    occupied = db.query(models.Booking.room_id).filter(
        models.Booking.status == "confirmed",
        models.Booking.check_in < check_out,
        models.Booking.check_out > check_in
    ).all()

    occupied_room_ids = [room_id for (room_id,) in occupied]

    if not occupied_room_ids:
        # If no rooms are occupied, just return all active rooms
        available_rooms = db.query(models.Room).filter(models.Room.is_active == True).all()
    else:
        # Otherwise, filter out the occupied ones
        available_rooms = db.query(models.Room).filter(
            ~models.Room.id.in_(occupied_room_ids),
            models.Room.is_active == True
        ).all()

    return available_rooms