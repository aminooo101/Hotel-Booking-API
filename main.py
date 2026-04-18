from fastapi import FastAPI
from routers import users
from database import Base, engine
import models



# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Booking API", version="1.0")
# Include the user router

app.include_router(users.router)


