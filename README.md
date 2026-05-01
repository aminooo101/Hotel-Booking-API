# 🏨 Hotel Booking API

Una API RESTful robusta y eficiente para la gestión de reservas de hotel, desarrollada con **FastAPI**, **SQLAlchemy** y **SQLite/PostgreSQL**. Incluye autenticación mediante JWT, validación de datos con Pydantic y un pipeline de Integración Continua (CI) con GitHub Actions.

---

## 🚀 Características

* **Gestión de Usuarios:** Registro e inicio de sesión de usuarios con contraseñas cifradas con `bcrypt`.
* **Seguridad:** Autenticación y autorización basada en tokens **JWT**.
* **Habitaciones:** Creación, visualización y gestión de habitaciones disponibles.
* **Reservas:** Creación de reservas con validaciones de fechas (evita reservas en fechas pasadas y conflictos de disponibilidad).
* **Base de Datos Flexible:** Configurada para funcionar con SQLite (desarrollo) o PostgreSQL (producción).
* **Tests Automatizados:** Cobertura completa de endpoints mediante `pytest` y `httpx`.

---

## 🛠️ Tecnologías utilizadas

* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Base de Datos:** SQLite / PostgreSQL
* **Validación de Datos:** Pydantic v2
* **Seguridad:** PyJWT, Passlib (Bcrypt)
* **Testing:** Pytest & HTTPX
* **Despliegue:** Docker & Render

---

## 📂 Estructura del Proyecto

```text
Hotel-Booking-API/
├── .github/workflows/
│   └── ci.yml               # Pipeline de GitHub Actions
├── main.py                  # Punto de entrada de la aplicación FastAPI
├── database.py              # Configuración de SQLAlchemy
├── models.py                # Modelos de la base de datos
├── schemas.py               # Esqueletos y validaciones de Pydantic
├── crud.py                  # Operaciones de base de datos
├── Dockerfile               # Configuración de Docker para el deploy
├── requirements.txt         # Dependencias del proyecto
├── test_main.py             # Tests unitarios y de integración
└── README.md                # Documentación del proyecto


