
---

# Store API (Flask + PostgreSQL)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-success?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A **RESTful API** built with **Flask** and **PostgreSQL**, designed to manage **stores, items, and tags**.
This project demonstrates modern API development practices including authentication, database migrations, and schema validation.

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

---

## 📂 Project Structure

```
.
├── app.py               # Main Flask application entry point
├── db.py                # Database initialization
├── blocklist.py         # Token revocation management
├── models/              # SQLAlchemy models (Store, Item, Tag, User)
├── resouces/            # Flask-Restful resources (endpoints)
├── schemas.py           # Marshmallow schemas for validation
├── migrations/          # Alembic migrations
├── requirements.txt     # Dependencies
└── .env.example         # Example environment variables
```

---

## 🛠️ Tech Stack & Skills

* **Flask** (API framework)
* **Flask-RESTful** (structured resources)
* **PostgreSQL** (relational database)
* **SQLAlchemy ORM**
* **Alembic** (migrations)
* **Marshmallow** (validation/serialization)
* **Flask-JWT-Extended** (authentication)
* **Environment configuration** with `.env`

---

## ⚡ Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/AliReza000J/rest-api-project.git
cd rest-api-project
```

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

### 6. Start the API

```bash
flask run
```

---

## 📌 Example API Endpoints

* **Register User** → `POST /register`
* **Login** → `POST /login`
* **Create Store** → `POST /store`
* **Get All Stores** → `GET /store`
* **Create Item** → `POST /item`
* **Assign Tag to Item** → `POST /item/{item_id}/tag/{tag_id}`

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

---

