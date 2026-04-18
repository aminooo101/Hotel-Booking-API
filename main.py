from fastapi import FastAPI
from routers import users
from database import Base, engine
import models



# Create the database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Hotel Booking API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Booking API"}

# Include the user router

app.include_router(users.router)


