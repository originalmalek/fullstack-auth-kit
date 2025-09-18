# Frontend Review & Recommendations

This document lists concrete issues found in `frontend/` and suggested fixes.

## Auth flow & navigation
- 401 redirects: `apiClient` falls back to `window.location.href` when refresh fails (full reload). Fix by calling `setGlobalRouter(router)` in a top-level client (e.g., `app/layout.tsx`) and remove the window fallback.
- Page unmounts on auth loading: Register and Forgot Password pages gate UI with `isLoading || isAuthenticated` and render a loader. If global auth state flips, forms remount and reset. Align with the Login page (don’t hide the form during checks; only redirect when authenticated).
- Reset password route: `app/(auth)/reset-password/[token]/page.tsx` treats `params` as `Promise` and resolves it in `useEffect`. In the App Router, `params` is synchronous or use `useParams()` in a client component.

## Forms & validation
- Native email tooltip: ensure all auth forms use `noValidate` (Login/Register/Forgot are set; consider adding to others for consistency).
- Duplicate prop: in `login-form.tsx` the password toggle `<Button>` has `size="sm"` twice.

## API layer & error handling
- Inconsistent router fallback: set the global router and remove `window.location.href` to avoid hard reloads.
- `auth.register` returns a mock response on error. Gate with an env flag or remove to avoid masking backend issues.

## State & types
- `auth-store.ts` → `checkAuth()` sets `isLoading` twice; clean up.
- `getUserFromToken()` returns `{ email: decoded.sub }`, but backend encodes `sub` as user id. Use `{ id: sub }` or stop pre-filling email from JWT.
- `auth-store.register()` calls `apiLogin` and returns an empty confirm URL. Implement real register or remove the method.

## UI/Accessibility
- Link/Button composition: several places wrap `<Button>` with `<Link>`, which yields `<a><button>…</button></a>`. Prefer `<Button asChild><Link …/></Button>` for valid markup and consistent styles.

## Quick wins
- Add `setGlobalRouter(router)` in a client wrapper (e.g., `layout.tsx`).
- Refactor `[token]` reset-password page to use `useParams()` and simplify loading states.
- Normalize error texts via a small mapper in the UI (already started) and align with backend error codes once standardized.
