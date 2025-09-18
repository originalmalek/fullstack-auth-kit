# Auth Starter (Backend + Frontend)

A minimal authentication starter for future projects:
- Backend: FastAPI + MongoDB (JWT auth, email verification, password reset)
- Frontend: Next.js + TypeScript + Tailwind (login, register, forgot/reset)

## Quick Start (Dev)
- Prerequisites: Python 3.11+, Node.js 20+, npm
- One command run:
  - `chmod +x servers.sh && ./servers.sh`
  - Frontend: http://localhost:3000
  - API: http://localhost:8000 (docs at `/docs`)

## Manual Setup
- Backend (from `backend/`):
  - Create venv: `python3 -m venv venv && source venv/bin/activate`
  - Install deps: `pip install -r requirements.txt`
  - Env: copy `backend/.env` and set values (see below)
  - Start: `uvicorn main:app --reload`
- Frontend (from `frontend/`):
  - Install deps: `npm install`
  - Env: `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - Start dev: `npm run dev`

## Environment Variables
- Backend (`backend/.env`):
  - `MODE=DEV` (enables test URLs below)
  - `MONGODB_NAME=auth` (required)
  - `MONGODB_TEST_URL=mongodb://localhost:27017`
  - `ROOT_TEST_URL=http://localhost:3000`
  - `JWT_SECRET_KEY=replace-me` and `SECRET_KEY=replace-me`
  - Mail (optional; set `MAIL_CONSOLE=true` to print emails):
    - `MAIL_CONSOLE=true`
    - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`
- Frontend: `.env.local`
  - `NEXT_PUBLIC_API_URL=http://localhost:8000`

## Project Structure
- `backend/` — FastAPI app (`main.py`, `routers/`, `utils/`, `templates/`)
- `frontend/` — Next.js app (`app/`, `components/`, `lib/`, `types/`)
- `servers.sh` — runs both servers in dev
- `AGENTS.md` — repo guidelines for contributors

## Notes
- Emails use HTML templates and can be printed to console with `MAIL_CONSOLE=true`.
- Error messages in the UI are normalized (e.g., login 401 → "Invalid email or password").
- Docker config was removed for now; can be reintroduced later.
