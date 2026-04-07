# PYQHUB FastAPI + React

A full-stack previous-year-question (PYQ) management app with:

- FastAPI backend (JWT auth, subject/paper APIs, file upload)
- React + Vite frontend
- SQLAlchemy ORM for database access
- Cloudinary for PDF storage

## Project Structure

```text
app/         # FastAPI backend
frontend2/   # React + Vite frontend
```

## Features

- Admin login with access + refresh JWT tokens
- Add subjects in bulk by semester
- Upload papers (PDF) with metadata
- Filter/fetch papers by semester and subject
- CORS-enabled API for local frontend development

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, python-jose, passlib, Cloudinary
- Frontend: React, Vite, React Router, Axios, Tailwind CSS
- Database: Configurable via `DB_URL` (SQLite/PostgreSQL/MySQL supported by SQLAlchemy URL)

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## 1) Backend Setup

From repository root:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Run backend:

```bash
cd app
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

## 2) Frontend Setup

In a new terminal:

```bash
cd frontend2
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Environment Variables

Set these in `.env`:

- `DB_URL` - SQLAlchemy DB URL
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (example: `HS256`)
- `USERNAME` - admin username
- `PASSWORD` - admin password
- `CLOUDINARY_CLOUD_NAME` - Cloudinary cloud name
- `CLOUDINARY_API_KEY` - Cloudinary API key
- `CLOUDINARY_API_SECRET` - Cloudinary API secret

## API Overview

- `POST /login` - Login and receive tokens
- `POST /refresh-token` - Refresh access token
- `POST /subjects` - Add subjects in bulk
- `GET /subject/{semester}` - List subjects for a semester
- `POST /add-paper` - Upload and store paper (protected)
- `POST /get-papers` - Retrieve papers by filters

## GitHub Readiness Checklist

- Secrets are ignored via `.gitignore`
- `.env.example` is included for safe onboarding
- `requirements.txt` and frontend `package.json` are committed
- Root README includes full setup instructions

## Suggested First Commit

```bash
git add README.md requirements.txt .env.example .gitignore app frontend2
git commit -m "Initialize full-stack PYQHUB project"
```

## Notes

- If CORS issues occur, confirm frontend URL matches allowed origins in `app/main.py`.
- Do not commit your real `.env` file.
