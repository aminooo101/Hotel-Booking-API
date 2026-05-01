# test_main.py
from fastapi.testclient import TestClient
from main import app
import uuid  # Para generar emails únicos en cada ejecución

client = TestClient(app)

def unique_email(base: str) -> str:
    # Genera un email único como user_1234@hotel.com
    return f"{base}_{uuid.uuid4().hex[:4]}@hotel.com"

# TEST 1
def test_register_user():
    email = unique_email("nuevo_usuario")
    response = client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "guest"
    })
    assert response.status_code == 201
    assert response.json()["email"] == email

# TEST 2
def test_register_duplicate_user():
    email = unique_email("duplicado")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "guest"
    })  

    response = client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "guest"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# TEST 3
def test_login_success():
    email = unique_email("login_exitoso")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "guest"
    })

    response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# TEST 4
def test_login_wrong_password():
    email = unique_email("login_fallido")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "guest"
    })

    response = client.post("/auth/login", data={
        "username": email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401

# TEST 5
def test_create_room():
    email = unique_email("admin")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })

    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    response = client.post("/rooms/", json={
        "number": uuid.uuid4().hex[:4], # Número único de habitación
        "type": "standard",
        "price": 100.0
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201

# TEST 6
def test_create_booking():
    email = unique_email("admin_booking")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })  

    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    room_response = client.post("/rooms/", json={
        "number": uuid.uuid4().hex[:4],
        "type": "standard",
        "price": 100.0
    }, headers={"Authorization": f"Bearer {access_token}"})
    room_id = room_response.json()["id"]

    response = client.post("/bookings/", json={
        "room_id": room_id,
        "check_in": "2026-08-01",
        "check_out": "2026-08-05",
        "status": "confirmed"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    assert response.json()["room_id"] == room_id
    # Cambiado a 'total_price' para coincidir con tu BookingResponse schema
    assert response.json()["total_price"] == 400.0

# TEST 7
def test_create_booking_previous_dates():
    email = unique_email("admin_booking")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })  

    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    room_response = client.post("/rooms/", json={
        "number": uuid.uuid4().hex[:4],
        "type": "standard",
        "price": 100.0
    }, headers={"Authorization": f"Bearer {access_token}"})
    room_id = room_response.json()["id"]

    response = client.post("/bookings/", json={
        "room_id": room_id,
        "check_in": "2022-08-01",
        "check_out": "2022-08-05",
        "status": "confirmed"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 400
    # Cambiado para coincidir con el mensaje exacto de tu API
    assert response.json()["detail"] == "Check-in cannot be in the past"

# TEST 8
def test_create_booking_availability():
    email = unique_email("admin_booking")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })  
    
    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    room_response = client.post("/rooms/", json={
        "number": uuid.uuid4().hex[:4],
        "type": "standard",
        "price": 100.0
    }, headers={"Authorization": f"Bearer {access_token}"})
    room_id = room_response.json()["id"]

    # Primer reserva
    client.post("/bookings/", json={
        "room_id": room_id,
        "check_in": "2026-10-10",
        "check_out": "2026-10-15",
        "status": "confirmed"
    }, headers={"Authorization": f"Bearer {access_token}"})

    # Segunda reserva (solapada)
    response = client.post("/bookings/", json={
        "room_id": room_id,
        "check_in": "2026-10-12",
        "check_out": "2026-10-17",
        "status": "confirmed"
    }, headers={"Authorization": f"Bearer {access_token}"})

    # Asserts corregidos
    assert response.status_code == 400
    assert response.json()["detail"] == "Room already booked for these dates"
# TEST 9
def test_get_my_bookings():
    email = unique_email("admin_booking")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })  
    
    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    # Cambiado a /bookings/ que es el GET de tu API para listar reservas
    response = client.get("/bookings/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TEST 10
def test_cancel_booking():
    email = unique_email("admin_booking")
    client.post("/auth/register", json={
        "email": email,
        "password": "test123",
        "role": "admin"
    })  
    
    login_response = client.post("/auth/login", data={
        "username": email,
        "password": "test123"
    })
    access_token = login_response.json()["access_token"]

    room_response = client.post("/rooms/", json={
        "number": uuid.uuid4().hex[:4],
        "type": "standard",
        "price": 100.0
    }, headers={"Authorization": f"Bearer {access_token}"})
    room_id = room_response.json()["id"]

    booking_response = client.post("/bookings/", json={
        "room_id": room_id,
        "check_in": "2026-11-01",
        "check_out": "2026-11-05",
        "status": "confirmed"
    }, headers={"Authorization": f"Bearer {access_token}"})
    booking_id = booking_response.json()["id"]

    # Corregido: Cambiado a PUT /bookings/{id}/cancel
    response = client.put(f"/bookings/{booking_id}/cancel", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"