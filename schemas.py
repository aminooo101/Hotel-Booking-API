from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional



class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[str] = "guest"
    
class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True
        
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoomCreate(BaseModel):
    number: str
    type: str
    price: float
    
class RoomResponse(BaseModel):
    id: int
    number: str
    type: str
    price: float
    is_active: bool

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date 
    
class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    status: str
    total_price: float

    class Config:
        from_attributes = True
        
        
    