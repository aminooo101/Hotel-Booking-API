from operator import index

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from database import Base
from sqlalchemy.orm import relationship





class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    role = Column(String, default = "guest")
    bookings = relationship("Booking", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer,primary_key=True, index = True)
    number = Column(String)
    type = Column(String)
    price = Column(Float)
    is_active = Column(Boolean,default=True)
    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer,primary_key=True, index = True  )
    user_id = Column(Integer,ForeignKey("users.id"))
    room_id = Column(Integer,ForeignKey("rooms.id"))
    check_in = Column(Date, nullable = False)
    check_out = Column(Date, nullable = False)
    status = Column(String, default = "confirmed")
    total_price = Column(Float)
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
