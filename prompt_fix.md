# How I stopped the login form from “reloading” and resetting

Context: On failed login, the page looked like it refreshed and the form cleared. Root causes were component unmounts during auth checks and an interceptor redirect on 401.

What I changed (apply these patterns to other projects)

1) Keep the form mounted during auth checks
- Problem: The login page returned a loader when `isLoading || isAuthenticated`, which unmounted the form while the store toggled `isLoading`.
- Fix: Remove the loader gate; keep the form visible, and only redirect after a confirmed success.
  - Before:
    - `if (isLoading || isAuthenticated) return <Loader/>` (form unmounts/resets)
  - After:
    - Keep the form rendered; use `useEffect` to `router.replace('/settings')` only when `isAuthenticated` becomes true.

2) Prevent interceptor from redirecting on the login 401
- Problem: Axios response interceptor handled every 401 (incl. `/auth/login`) by attempting refresh or redirecting (sometimes via `window.location`, causing a full reload).
- Fix: Detect login request and short‑circuit:
  - If `error.response?.status === 401` and `originalRequest.url.includes('/auth/login')`, just `return Promise.reject(new Error('Invalid email or password'))` — no refresh attempts, no redirects.
  - For other 401s, you may still refresh; if refresh fails, prefer client router navigation over `window.location`.

3) Show a controlled, inline error instead of navigating
- In the form submit `catch`, set local error state and render an alert.
- Normalize messages (e.g., map any 401/invalid/unauthorized to “Invalid email or password”).

4) Disable native HTML validation popups (optional but consistent)
- Add `noValidate` to the `<form>` to avoid browser tooltips overriding your UI messages.

5) Avoid full reloads from global navigation
- If you need to navigate from an interceptor, inject the Next.js router instead of using `window.location`.
  - Example: expose `setGlobalRouter(router)` from your API client and call it in a top‑level client (e.g., `app/layout.tsx`). Use `router.push('/login')` in the interceptor fallback.

Minimal reference snippets

- Interceptor guard for login 401:
```ts
const isLogin = typeof originalRequest.url === 'string' && originalRequest.url.includes('/auth/login');
if (error.response?.status === 401 && isLogin) {
  return Promise.reject(new Error('Invalid email or password'));
}
```

- Login page logic:
```ts
useEffect(() => {
  if (isAuthenticated) router.replace('/settings');
}, [isAuthenticated]);
// Do not early-return a loader on isLoading; keep the form mounted
```

- Form submit with inline error:
```ts
const onSubmit = async (data) => {
  try { await login(data); router.push('/'); }
  catch (e) { setError('Invalid email or password'); }
};
```
