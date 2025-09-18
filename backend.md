# Backend Review & Recommendations

This document highlights potential issues and targeted improvements for the FastAPI backend under `backend/`.

## Configuration & Secrets
- Problem: `Settings` mutates `MONGODB_URL` via `.replace("<PASSWORD>", ...)` and assumes the placeholder exists. Missing vars may yield `NoneType` errors.
- Improve: Validate required envs at startup; fail fast with clear messages. Prefer a single `MONGODB_URI` already containing credentials.
- Problem: `MODE == 'DEV'` toggles URLs but leaves other secrets unchanged.
- Improve: Use a single `.env` schema across modes; consider `pydantic-settings` for typed validation.

## Database Layer
- Problem: `utils/db.py` uses global singletons initialized by `init_database()`, but `utils/tasks.py` creates a new client per call (connection churn).
- Improve: Centralize DB access: reuse the app-level client (e.g., expose `get_database()` from `utils/db.py`) everywhere, including tasks.
- Problem: `users_collection` can be `None` if used before startup.
- Improve: Guard access or inject collection via dependency (`Depends`) to avoid None access during tests/CLI.

## Auth & Tokens
- Problem: Mixed token handling: AuthX for access/refresh, manual `jose.jwt` for reset/confirm; no token revocation/rotation after password change.
- Improve: Unify token lib usage; revoke/rotate refresh tokens on password change; set shorter expirations for magic links.
- Problem: Login returns 403 for unconfirmed email (OK), but messages are user-visible—ensure i18n or stable API error codes.

## Email & Background Tasks
- Problem: `workers/email_processor.py` retries, but errors are only printed; SMTP settings lack TLS/mode flexibility.
- Improve: Structured logging; configurable retry/backoff; support STARTTLS; capture failures in `processing_tasks` with reasons.
- Problem: `load_email_template()` reads from disk per send.
- Improve: Cache templates in memory.

## Rate Limiting
- Problem: `slowapi` limiter uses client IP; behind proxies it may see gateway IPs.
- Improve: Use X-Forwarded-For extraction or Starlette `ProxyHeadersMiddleware`.

## Health Endpoints
- Problem: `/health/detailed` references `settings.OPENAI_API_KEY` which is not defined in `Settings`.
- Improve: Add optional `OPENAI_API_KEY` to `Settings` or remove that check.
- Problem: `/mail/verify/{token}` returns 200 with error detail for already confirmed email.
- Improve: Return 200 JSON message without raising HTTPException, or return 409.

## Data Model & Validation
- Problem: Password policy not enforced server-side; only hashing on insert.
- Improve: Add minimal password rules (length) in `UserCreate` or separate schema for registration.
- Problem: `RegisterResponse.email_task_id` marked required but may be absent if mail queueing fails.
- Improve: Mark optional or handle failure path explicitly.

## Security
- Problem: CORS allows `*` with credentials enabled.
- Improve: Restrict origins to configured list.
- Problem: Email templates include product names hardcoded ("SummarMe").
- Improve: Use settings for branding/links.

## Consistency & Errors
- Problem: `utils.tasks.get_database()` creates a new client; `utils.db.get_database()` returns global—two patterns.
- Problem: Mixed exception styles: sometimes `raise HTTPException`, sometimes swallow/log.
- Improve: Standardize error handling and logging. Add structured logs for audits.

## Suggested Action Items
- Add `.env.example` with required/optional vars.
- Refactor DB access in `utils/tasks.py` to reuse shared client.
- Add `OPENAI_API_KEY: Optional[str]` to `Settings` or remove check.
- Tighten CORS `allow_origins` from environment.
- Add server-side password constraints and consistent API error shapes.
- Cache email templates and add STARTTLS option.
- Use `ProxyHeadersMiddleware` if deployed behind a proxy.
