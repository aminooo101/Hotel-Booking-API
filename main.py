from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, bookings, rooms
from database import Base, engine
import models
from fastapi.security import OAuth2PasswordBearer

# Create the database tables. In a production environment, consider using Alembic for migrations.
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app = FastAPI(title="Hotel Booking API", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking API"}

# Include the routers
app.include_router(users.router)
app.include_router(bookings.router) 
app.include_router(rooms.router)





