
---

# Store API (Flask + PostgreSQL)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-success?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Deployed-brightgreen)

A **RESTful API** built with **Flask** and **PostgreSQL**, designed to manage **stores, items, and tags**.  
This project demonstrates modern API development practices including authentication, database migrations, and schema validation. 
It also includes **user registration with email verification** using Maileroo.

🌍 **Live API on Render:**  
👉 [https://rest-api-project-q1zn.onrender.com](https://rest-api-project-q1zn.onrender.com)  

⚡ The API does not include a frontend UI. You can explore and test it using:
- [Swagger UI](https://rest-api-project-q1zn.onrender.com/swagger-ui)  
- **Postman** or **Insomnia** REST clients  

---

## 🚀 Features

* **Flask-based REST API** following best practices.
* **PostgreSQL database** with SQLAlchemy ORM.
* **Alembic migrations** for schema version control.
* **JWT authentication** for secure endpoints.
* **CRUD operations** for:
  * Stores
  * Items
  * Tags
  * Users
* **Marshmallow schemas** for input/output validation.
* **Blocklist** support for token revocation (logout).
* Organized **resources and models** structure.
* User registration with **email verification** (Maileroo API)
* Support for **background tasks / queue workers** (currently disabled in Render free tier, but fully implemented in code)

---

## 📂 Project Structure

```

.
├── app.py                     # Application factory (create_app)
├── db.py                      # Database initialization
├── blocklist.py               # Token revocation (logout) management
├── models/                    # SQLAlchemy models (Store, Item, Tag, User)
├── resources/                 # Flask-Smorest resource endpoints
├── schemas.py                 # Marshmallow schemas for validation / serialization
├── settings.py                # Configuration / settings (e.g. env-based config)
├── tasks.py                   # Background tasks / queue worker definitions
├── templates/                 # Email templates (for verification)
│   └── email/
├── migrations/                # Alembic migrations folder
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── Procfile                   # For deployment (specifies processes)
└── .flaskenv                  # Flask environment variables (development)

````

---

## 🛠️ Tech Stack & Skills

* **Flask** (API framework)
* **Flask-Smorest** (blueprint-based resources)
* **PostgreSQL** (relational database)
* **SQLAlchemy ORM**
* **Alembic** (migrations)
* **Marshmallow** (validation/serialization)
* **Flask-JWT-Extended** (authentication)
* **Environment configuration** with `.env`
* **Maileroo API** (email verification)

---

## ⚡ Quickstart (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/AliReza000J/rest-api-project.git
cd rest-api-project
````

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file (see `.env.example`) with:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your_secret_key
```

### 5. Run database migrations

```bash
flask db upgrade
```

### 6. Start the API locally

```bash
flask run
```

---

## 📌 Example API Endpoints

* **Register User** → `POST /register`
  > On successful registration, a verification email is automatically sent to the provided email address.
* **Login** → `POST /login`
* **Create Store** → `POST /store`
* **Get All Stores** → `GET /store`
* **Create Item** → `POST /item`
* **Assign Tag to Item** → `POST /item/{item_id}/tag/{tag_id}`

📖 Full interactive docs available at:
👉 [Swagger UI](https://rest-api-project-q1zn.onrender.com/swagger-ui)

---

## 🎯 Highlights

This project demonstrates:

* Building **REST APIs** with Flask.
* Structuring a **production-ready backend**.
* Handling **database migrations** with Alembic.
* Implementing **JWT authentication** and **token revocation**.
* Using **schemas** for validation and clean data handling.

---

## 🔮 Future Improvements

* **Docker support** → containerize the app for easier deployment.
* **Unit & integration testing** → add coverage with `pytest` and `Flask-Testing`.
* **CI/CD pipeline** → automate testing & deployment with GitHub Actions.
* **Role-based access control (RBAC)** → extend user management.
* **Caching & performance optimization** → Redis or Flask-Caching.
* **Monitoring & logging**

---

## ⚠️ Notes

Background task queue and worker are implemented but disabled on Render free tier. 
To enable them, configure a Redis instance and run the worker service.
