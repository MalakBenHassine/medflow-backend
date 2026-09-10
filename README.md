# medflow-backend

Backend (Django REST Framework + PostgreSQL) for **Assistant Médical Intelligent**, a multi-tenant clinic management platform: patient records, consultations, billing, and role-based access control.

Pairs with the Next.js frontend: [Med-Flow-Front](https://github.com/MalakBenHassine/Med-Flow-Front).

## Stack

Python, Django, Django REST Framework, PostgreSQL

## Getting started

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Configure your database and secrets via environment variables (see `.env.example` if present, or your local Django settings) — do not commit a real `.env` file to this repository.
