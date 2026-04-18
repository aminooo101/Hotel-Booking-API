from datetime import date
from requests import Session
from fastapi import Depends
import models
from database import get_db


def get_available_rooms(
    check_in:date,
    check_out:date,
    db: Session = Depends(get_db)
):

    occupied = db.query(models.Booking.room_id).filter(
        models.Booking.status == "confirmed",
        models.Booking.check_in < check_out,
        models.Booking. check_out > check_in
    ).all()

    occupied_room_ids = [room_id for (room_id,) in occupied]

    available_rooms = db.query(models.Room).filter(
        ~models.Room.id.in_(occupied_room_ids)
        models.Room.is_active == True
    ).all()
    return available_rooms



