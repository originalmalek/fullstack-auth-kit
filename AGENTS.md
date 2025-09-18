# Repository Guidelines

## Project Structure & Module Organization
- `backend/` — FastAPI service. Key folders: `routers/` (API routes), `models/` (Pydantic models), `utils/` (config, db, security, mail, tasks), `workers/` (background jobs), `templates/` (email/html), entrypoint `main.py`.
- `frontend/` — Next.js (TypeScript + Tailwind). Key folders: `app/` (routes/pages), `components/` (UI + features), `lib/` (API clients, stores, utils), `types/`.
- Env files: `backend/.env`, `frontend/.env.local`. Do not commit secrets.

## Build, Test, and Development Commands
- Backend (from `backend/`):
  - Setup: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - Run API (dev): `uvicorn main:app --reload`
- Frontend (from `frontend/`):
  - Install: `npm install`
  - Dev server: `npm run dev`
  - Build/Start: `npm run build && npm start`
  - Lint: `npm run lint`
  - Tests: `npm run test` (UI: `npm run test:ui`, coverage: `npm run test:coverage`)

## Coding Style & Naming Conventions
- Python: PEP 8, 4‑space indent, type hints where practical. Files/modules `snake_case`, classes `PascalCase`, functions/vars `snake_case`. Keep route files in `routers/` (e.g., `routers/auth.py`).
- TypeScript/React: ESLint + Prettier enforced. Components `PascalCase` (files typically `kebab-case.tsx`, e.g., `login-form.tsx`). Vars/functions `camelCase`. Prefer co-located component-specific helpers.

## Testing Guidelines
- Frontend: Vitest + Testing Library. Place tests near code: `*.test.ts`/`*.test.tsx`. Aim for meaningful unit tests around `lib/` and component behavior; use `happy-dom`/MSW for mocks.
- Backend: No test suite configured. If adding tests, use `pytest` with `tests/` and `test_*.py` pattern (add `pytest` to `requirements.txt`).

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `build:`. Imperative, present tense; include scope when helpful (e.g., `feat(auth): add refresh token`).
- PRs: concise description, linked issue, setup/verification steps, and screenshots/GIFs for UI changes. Keep changes focused and incremental.

## Security & Configuration Tips
- Backend required env (examples in `backend/.env`): `MONGODB_URL`, `MONGODB_PASSWORD`, `MONGODB_NAME`, `ROOT_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, mail settings (`MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`, `MAIL_PORT`), optional `MODE`, `MONGODB_TEST_URL`, `ROOT_TEST_URL`, and `OPENAI_API_KEY` if used.
- Never log secrets. Validate configs via health endpoints under `/health`.
