# Hotel Booking API

A RESTful API for managing hotel rooms and bookings, built with FastAPI, SQLAlchemy, and Pydantic. Includes JWT authentication, date validation, automated tests, Docker support, and a GitHub Actions CI pipeline.

## Features

- User registration and login with bcrypt-hashed passwords
- JWT-based authentication and authorization
- Room management (create, list)
- Booking creation with date conflict and past-date validation
- SQLite for local development (PostgreSQL-ready)
- Full test suite with pytest and httpx
- Docker support and GitHub Actions CI

## Tech Stack

- FastAPI
- SQLAlchemy + Pydantic v2
- PyJWT + Passlib (bcrypt)
- pytest + httpx
- Docker

## Project Structure

```
Hotel-Booking-API/
├── .github/workflows/ci.yml    # GitHub Actions CI
├── main.py                     # FastAPI entry point
├── database.py                 # SQLAlchemy setup
├── models.py                   # Database models
├── schemas.py                  # Pydantic schemas
├── crud.py                     # Database operations
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Dependencies
├── test_main.py                # Automated tests
└── README.md
```

## Installation & Run

```bash
git clone https://github.com/aminooo101/Hotel-Booking-API
cd Hotel-Booking-API
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000/docs for the interactive Swagger UI.

## How to Run the Tests

The project includes a full test suite covering registration, login, room creation, booking creation, date validation, availability conflicts, and cancellation.

```bash
# Make sure you are in the project root with the virtual environment activated
pytest test_main.py -v
```

Expected result: all tests pass (currently 10 tests covering the main endpoints and edge cases).

## Docker

```bash
docker build -t hotel-api .
docker run -p 8000:8000 hotel-api
```

## Author

Amin Hadian · [github.com/aminooo101](https://github.com/aminooo101) · [linkedin.com/in/amin-hadian-841277204](https://www.linkedin.com/in/amin-hadian-841277204)
