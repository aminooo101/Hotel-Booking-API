from fastapi import APIRouter, Depends, HTTPException # Added APIRouter
from datetime import date
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import oauth2_scheme , get_current_user


# 1. Create the router object
router = APIRouter(prefix="/bookings", tags=["bookings"])

# 2. Add the decorator @router.get
@router.get("/available")
def get_available_rooms(
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    # Create a subquery for IDs of rooms that have overlapping confirmed bookings
    occupied_subquery = db.query(models.Booking.room_id).filter(
        models.Booking.status == "confirmed",
        models.Booking.check_in < check_out,
        models.Booking.check_out > check_in
    )

    # Fetch rooms that are active and not in the occupied subquery
    available_rooms = db.query(models.Room).filter(
        models.Room.is_active == True,
        ~models.Room.id.in_(occupied_subquery)
    ).all()

    return available_rooms