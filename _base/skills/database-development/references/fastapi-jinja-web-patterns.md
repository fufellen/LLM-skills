# FastAPI + Jinja2 web-CRUD patterns

Reusable patterns and traps from building an admin web app on top of the default database-development stack (FastAPI + Jinja2 + PostgreSQL + Caddy on a VPS). Load this reference when building or debugging a similar app.

## Templates

### TemplateResponse: use kwargs, not the legacy dict signature

Wrong (works with old Starlette, silently breaks on current versions):

```python
return templates.TemplateResponse("page.html", {"request": request, ...})
```

Fails with `TypeError: unhashable type: 'dict'` deep inside Jinja's template cache — the dict is being used as a cache key. Trap: the traceback points at Jinja internals, not your call site.

Correct:

```python
return templates.TemplateResponse(request=request, name="page.html", context={...})
```

### Register template globals for cross-page widgets

Anything called from `base.html` on every render (badge counts, permission checks, current user) belongs in `templates.env.globals`, not in every route's context dict. One place to add, zero routes to touch:

```python
templates.env.globals["current_user"] = lambda r: current_user(r)
templates.env.globals["pending_count"] = _pending_confirmations_count
```

Call in template as `{% set u = current_user(request) %}`.

## CSS/HTML

### `body > nav`, not `nav`, for a top-level sidebar

A bare `nav { position: fixed; ... }` in base.html **also** styles `<nav class="tabs">` used inside a page template — the tabs collapse into invisible fixed elements. Use the direct-descendant selector when the rule targets the top-level nav:

```css
body > nav { position: fixed; left: 0; top: 0; bottom: 0; ... }
body > nav a { ... }   /* not `nav a` */
```

Same applies to any HTML5 landmark element (`main`, `header`, `footer`) used both structurally and semantically inside content.

### Vertical form class: `.box.stack`

Default `<form class="box"><label>X <input></label>...</form>` renders as tight rows because inline-block labels flow left-to-right. For a top-to-bottom form (usual expectation for data-entry), keep the base class and add a modifier:

```css
form.box { background:#fff; border:1px solid #ddd; padding:.8rem; }
form.box label { display: inline-block; margin: .2rem .8rem .2rem 0; }
/* stacked variant */
form.box.stack label { display: block; margin: .5rem 0 .15rem; font-weight: 600; }
form.box.stack input:not([type=checkbox]):not([type=radio]),
form.box.stack textarea,
form.box.stack select { display:block; width:100%; max-width: 24rem; padding:.35rem; }
```

Toggling `stack` in the template alone flips the whole form vertical.

### Sidebar as an off-canvas drawer

Minimal admin-panel drawer without a framework. HTML in `base.html`:

```html
<button class="nav-toggle" id="navToggle">☰</button>
<div class="nav-backdrop" id="navBackdrop"></div>
<nav id="nav"> <div class="menu">…links…</div> </nav>
<script>
  const b = document.body, close = () => b.classList.remove('nav-open');
  navToggle.onclick = e => { e.stopPropagation(); b.classList.toggle('nav-open'); };
  navBackdrop.onclick = close;
  addEventListener('keydown', e => e.key === 'Escape' && close());
</script>
```

CSS: nav is `position:fixed; transform:translateX(-100%); transition:transform .18s;` by default; `body.nav-open > nav { transform: translateX(0) }` slides it in. Backdrop is `position:fixed; inset:0; opacity:0; pointer-events:none;` and gets `opacity:1; pointer-events:auto` when open. z-index: backdrop 15, nav 20, toggle 30 (button stays clickable when nav is open, closes-on-click on backdrop). Give `main` a `padding-top` at least the toggle button's height so it doesn't overlap first-row content.

### Print without a PDF library

Most «сохранить/распечатать отчёт» requirements are served by browser print + a `@media print` block that hides chrome:

```css
@media print {
  nav, .print-hide { display: none !important; }
  main { max-width: none; margin: 0; padding: 0; }
}
```

Trigger with `<button onclick="window.print()">Печать</button>`. User picks «Save as PDF» in the OS dialog. Works on desktop, Android, iOS.

## Auth middleware

### `PUBLIC_PATHS` + `PUBLIC_PREFIXES` (exact + startswith)

An auth gate that only checks exact paths breaks on `/static/*` and other tree-mounted resources. Keep two containers:

```python
PUBLIC_PATHS = {"/login", "/logout", "/api/login", "/sw.js", "/manifest.webmanifest"}
PUBLIC_PREFIXES = ("/static/",)

@app.middleware("http")
async def _auth_gate(request, call_next):
    path = request.url.path
    if path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)
    ...
```

When you add a new public endpoint (PWA-related is the most common case), remember to add it to `PUBLIC_PATHS`, otherwise the gate returns 303 → `/login` before the route runs. Symptom: POST `/api/…` returns the HTML of the login page with 200.

### Route allowed ≠ links shown

If middleware lets a limited role reach a route in read-only mode, the template must **not** render action links that would send that role somewhere else the middleware blocks. Otherwise the UI 303s them on every click. Pass the role into the template and hide links:

```jinja
{% set is_teacher = u and u['role'] == 'teacher' %}
{% if is_teacher %}{{ l['grp'] }}{% else %}<a href="/groups/{{ l['group_id'] }}">{{ l['grp'] }}</a>{% endif %}
```

Middleware protects security, template protects UX. Both, always.

## Data model

### Role of access ≠ HR job title

Two orthogonal fields. `users.role ∈ {owner, admin, teacher}` drives what the app allows. `teachers.job_title` (нейропсихолог/логопед/тренер) is free-text on the person record, only used for reports and time sheets. Do not overload one field for both — the stakeholder will change one without wanting to change the other, and you'll break auth.

### Per-relationship pricing, not per-catalogue

For services where each client-service-professional triple has its own price/discount/margin (typical for tutoring, therapy, coaching, small clinics), put pricing on the `enrollments` (client, professional, service) row itself:

- `unit_price` — snapshot in `enrollment_tariffs(enrollment_id, duration_min, price)`.
- `discount_percent smallint` + `discount_reason text` on the enrollment.
- `center_share_percent smallint` on the enrollment — percent the business keeps; professional gets `100 - N`.

Payout SQL then joins `lessons → lesson_participants → enrollments` and computes `lp.price * (100 - COALESCE(e.center_share_percent, DEFAULT)) / 100`. `COALESCE` shields legacy rows from a later-added column.

Trap: don't try to define a single «formula for everyone». If the stakeholder says «под всех подогнать нельзя», the model must expose the per-enrollment knob directly, not fake averages.

### Time sheet as a query, not a table

An HR time sheet (rows: professionals, columns: days, cells: hours worked) is a pure aggregation over `lessons WHERE status='held'`. Recomputing on every render is fast enough well past thousands of lessons. Do not add a `time_sheet` table — you'll create a second source of truth that drifts from `lessons`.

## Notifications

### Three-layer plan for «remind me before event X»

1. **In-app widget + navbar badge** — SQL count of «past but not yet confirmed» rows, rendered on every page via a template global. First line of defense, works even if nothing else is wired.
2. **PWA + Web Push (VAPID + service worker)** — 3 files (`/manifest.webmanifest`, `/sw.js` served at root scope, icon PNGs). Works on desktop, Android; iOS 16.4+ needs the site added to Home Screen. Cover 95% of «нужно нативное приложение» requests without shipping an APK/IPA.
3. **Desktop companion** (PySide6 + PyInstaller `--onefile`) — only when the requirement is truly «окно поверх всех программ» on a specific admin PC, which browsers can't do. Reuses same login and same JSON API.

Prefer 1+2 first; add 3 only when the specific user's specific PC needs it. Skip SMS/messenger channels unless the venue-specific gateway is already free/available; they're per-message paid and add integrations without materially better UX than 2.

### `Service-Worker-Allowed: /` header

Serving `sw.js` from `/static/sw.js` scopes it to `/static/*` and it can't intercept push at the site root. Serve it from `/sw.js` (its own FastAPI route returning `FileResponse`) with `headers={"Service-Worker-Allowed": "/", "Cache-Control": "no-cache"}`.

### Action buttons in push

Payload includes an id needed to identify the event; `sw.js` shows `notification.actions` conditionally (only when payload has that id — test/generic pushes get plain notification). Handler POSTs to a `/api/…/quick-status` endpoint with `credentials: 'include'` — same session cookie as the browser tab. iOS silently ignores `actions` and falls back to click-through; design for that.

## PostgreSQL specifics

### `date + time` combines into `timestamp` in a query

For an event scheduled by `lesson_date DATE` and `start_time TIME`, filter «starts within N minutes» directly in SQL, don't compute in Python:

```sql
WHERE (lesson_date + start_time) BETWEEN %s AND %s   -- %s = timestamp
```

Cross-timezone gotcha: the sum is `timestamp` (without zone). If your app timezone matters, cast: `((lesson_date + start_time) AT TIME ZONE 'Europe/Moscow')`.

### `TRUNCATE … RESTART IDENTITY CASCADE` for a demo-data wipe

Cleanest way to reset a schema before handing it to the real customer: list the tables you want empty, `RESTART IDENTITY` resets serial sequences to 1, `CASCADE` handles foreign-key referents. Keep `users` and any settings table out of the list — the customer still needs to log in. Take a `pg_dump -Fc` first so the wipe is one `pg_restore` away.

## Deployment

### One-command deploy script that reads env

`deploy/update.sh` on the server: `git pull`, `pip install -r requirements.txt`, run migrations. Migrations need env vars (DB URL). Load them at the top:

```bash
set -a; . /etc/tutor-center.env; set +a
```

Without this, migration scripts using `DATABASE_URL` fail with «password authentication failed» — env vars from systemd don't leak into a plain `bash deploy/update.sh` invocation.

### `.gitignore` for a PyInstaller-based companion app

If the same repo ships a desktop companion (`desktop/notifier.py` etc.), the 50 MB `.exe` and PyInstaller intermediates must not go into git:

```gitignore
desktop/build/
desktop/dist/
desktop/*.spec
desktop/.venv/
```

Ship a build recipe (`desktop/README.md`) instead; the maintainer rebuilds locally.
