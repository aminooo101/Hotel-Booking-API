# routers/rooms.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import require_admin, get_current_user
import models, schemas

router = APIRouter(prefix="/rooms", tags=["rooms"])

# 3. Load
@router.get("/", response_model=list[schemas.RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    # escribe tú: consulta todas las rooms en la BD
    rooms = db.query(models.Room).all()
    # return
    return rooms

# 2. CREAR — solo admin
@router.post("/", response_model=schemas.RoomResponse, status_code=201)
def create_room(
    room: schemas.RoomCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_admin)
):
    # - crear objeto models.Room con los datos de room
    new_room = models.Room(number=room.number,price=room.price,type=room.type)
    # - añadir a la BD
    db.add(new_room)
    # - commit y refresh
    db.commit()
    db.refresh(new_room)
    # - return
    return new_room

# 3. VER UNA habitación por id
@router.get("/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# 4. MODIFICAR — precio, tipo, estado
@router.put("/{room_id}", response_model=schemas.RoomResponse)
def update_room(
    room_id: int, 
    room: schemas.RoomCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    # pista: primero busca la habitación, luego modifica sus campos
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db_room.number = room.number
    db_room.price = room.price
    db_room.type = room.type
    db.commit()
    db.refresh(db_room)
    return db_room


@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return None
