# FastAPI Project

This repository contains a backend project built with **FastAPI**, **SQLAlchemy**, and **Alembic**.  
The goal is to explore backend tooling, with a focus on database modeling, migrations, authentication, and API design.

The project is **focused on Android integration** and serves as a **simple school management system** that handles:

- Assignments
- Submissions

---

## Development Notes

The `table_crud` module was created to easily insert data into the database during development, without needing to open **pgAdmin**.  
It provides helper functions for adding initial or test data.

> ⚠️ This module is **only for testing** and will be removed later.

---

## Features

- **Authentication**

  - JWT-based access tokens
  - Refresh token support
  - Scope-based endpoint protection

- **Database**

  - Full table schema defined in `dmmodel.py` (kept in one place since this is the first project)
  - Database migrations handled using **Alembic**

- **Email Integration**
  - When an admin registers a new user, the system automatically sends an email containing login credentials

---

## Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy 2.0** – ORM with async support
- **Alembic** – Database migrations
- **PostgreSQL** – Database
- **JWT** – Authentication
- **SMTP** – Email notifications
