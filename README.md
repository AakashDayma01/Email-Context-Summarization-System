# Email Context & Summarization System

## Overview

The Email Context & Summarization System is a backend application developed as part of the Ascend Backend Engineer Case Study.

The system provides a unified view of all email conversations between accountants and clients within a CPA firm. It allows multiple accountants working for the same client to view previous conversations, avoid asking duplicate questions, and generate AI-powered summaries of email threads.

Instead of integrating with Microsoft Graph API, this project uses seeded mock email data to simulate real-world email conversations.

---

# Features

## Authentication

* JWT Authentication using Simple JWT
* Session-based login for web dashboard
* Role-based authorization

---

## Firms

* Multiple CPA firms
* Each firm has multiple accountants
* Firm-aware access control

---

## Accountants

* Admin
* Accountant
* Superuser

---

## Clients

* View client list
* View client details
* Firm-wise client isolation

---

## Email Conversations

* Store email history
* View complete email thread
* Add new mock emails
* Simulate incoming emails

---

## AI Email Summary

Generate intelligent summaries using Google Gemini when configured.

Summary contains:

* Actors involved
* Concluded discussions
* Open action items

If Gemini is not configured or the API call fails, the app falls back to a local mock summary implementation.

---

## Encryption

Generated summaries are encrypted before storing in PostgreSQL.

No summary is stored in plain text.

---

## Caching

Summary responses are cached in Redis.

If a cached summary exists, the app returns it directly. If not, it reads the DB or generates a new summary, stores it in Redis, and returns it.

---

## Reports

### Firm Admin

Can view

* Total clients
* Clients with generated summaries

### Superuser

Can view

* Summary count grouped by firm

---

## Tracking

Each generated summary stores

* Emails processed
* Last refreshed timestamp

---

# Tech Stack

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Google Gemini API
* Simple JWT
* Fernet Encryption
* Django Cache Framework

---

# Project Structure

```
apps/
│
├── accounts/
├── clients/
├── emails/
├── firms/
├── reports/
└── summaries/

config/
│
├── settings/
├── urls.py
├── wsgi.py
└── asgi.py

templates/
static/
manage.py
requirements.txt
README.md
```

---

# Database Models

* Firm
* Account
* Client
* Email
* EmailSummary

---

# API Endpoints

## Authentication

POST

```
/api/token/
```

Refresh Token

```
/api/token/refresh/
```

---

## Clients

```
GET /api/clients/
GET /api/clients/<id>/
```

---

## Emails

```
GET /api/<client_id>/emails/
POST /api/add/<client_id>/
```

---

## Summary

Generate Summary

```
POST /api/<client_id>/summary/
```

Refresh Summary

```
POST /api/<client_id>/summary/refresh/
```

---

## Reports

Firm Report

```
GET /api/reports/api/
```

Global Report

```
GET /api/reports/api/global/
```

---

# Web Pages

Dashboard

```
/
```

Clients

```
/clients/
```

Client Details

```
/clients/<id>/
```

Reports

```
/reports/
/reports/firm/
/reports/global/
```

Summary Web Pages

```
/summary/generate/<id>/
/summary/refresh/<id>/
```

Login

```
/login/
```

Logout

```
/logout/
```

---

# Installation

Clone repository

```
git clone <repository-url>
```

Create virtual environment

```
python -m venv myvenv
```

Activate

Linux

```
source myvenv/bin/activate
```

Windows

```
myvenv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=email_context

DB_USER=postgres

DB_PASSWORD=psql

DB_HOST=localhost

DB_PORT=5432

GEMINI_API_KEY=your_gemini_api_key

ENCRYPTION_KEY=your_fernet_key
```

---

# Database Setup

Run migrations

```
python manage.py migrate
```

Seed mock data

```
python manage.py seed_emails
```

Create superuser

```
python manage.py createsuperuser
```

Run server

```
python manage.py runserver
```

/login/
```

Logout

```
/logout/
```

---

# Installation

Clone repository

```
git clone <repository-url>
```

Create virtual environment

```
python -m venv myvenv
```

Activate

Linux

```
source myvenv/bin/activate
```

Windows

```
myvenv\Scripts\activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=email_context

DB_USER=postgres

DB_PASSWORD=psql

DB_HOST=localhost

DB_PORT=5432

GEMINI_API_KEY=your_gemini_api_key

ENCRYPTION_KEY=your_fernet_key
```

---

# Database Setup

Run migrations

```
python manage.py migrate
```

Seed mock data

```
python manage.py seed_emails
```

Create superuser

```
python manage.py createsuperuser
```

Run server

```
python manage.py runserver
```

---

# User Roles

## Superuser

* View all firms
* View all clients
* View global reports

## Firm Admin

* View firm's clients
* Generate summaries
* View firm reports

## Accountant

* View assigned firm's clients
* View conversations
* Generate summaries

---

# Security

* JWT Authentication
* Role-based Authorization
* Encrypted Summary Storage
* CSRF Protection
* ORM-based Queries
* Password Hashing

---

# Performance Optimizations

* Summary Caching
* Optimized ORM Queries using `select_related()`
* Reusable Service Layer
* Mock Email Seeder
* Summary Refresh Endpoint

---

# Future Improvements

* Microsoft Graph API Integration
* Outlook Synchronization
* Background Summary Generation using Celery
* Email Notifications
* Elasticsearch for Email Search
* Audit Logs
* Docker Deployment
* CI/CD Pipeline
* Unit & Integration Tests

---

# Demonstration Flow

1. Login as Admin or Accountant.
2. View firm clients.
3. Open a client.
4. Review email conversations.
5. Generate AI summary.
6. Refresh summary.
7. Add a new mock email.
8. Regenerate summary.
9. Verify updated report counts.
10. Test role-based access with different users.

## Project Workflow

```text
User Login
      │
      ▼
JWT Authentication
      │
      ▼
Get Clients
      │
      ▼
Select Client
      │
      ▼
Fetch Emails
      │
      ▼
Check Redis Cache
      │
 ┌────┴────┐
 │         │
Hit       Miss
 │         │
 ▼         ▼
Return   Generate Summary (Gemini AI or Mock)
           │
           ▼
      Store Summary in Redis
           │
           ▼
 Encrypt Summary using Fernet
           │
           ▼
 Save Encrypted Summary in PostgreSQL
           │
           ▼
 Return Summary to User
```