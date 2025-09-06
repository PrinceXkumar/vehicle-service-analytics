# Architecture & Flow

High-level flow:
1. User authenticates (login/signup)
2. After login, `/dashboard` redirects by role to the correct dashboard view
3. Each dashboard queries relevant data and renders a template
4. Service workflows:
   - Customer: book a service → creates `Service`
   - Manager: assigns mechanic to pending `Service`
   - Mechanic: updates `Service.status`

Key decisions:
- Profiles in a separate model
  - Keeps `User` clean, supports multiple roles and profile data
- Signals to auto-create Profile
  - Reduces boilerplate; every user has a profile
- Decorator `role_required`
  - Clear guard rails for routes; prevents cross-role access
- Separate `Service` vs `ServiceRecord`
  - `Service`: operational workflow (booking/assign/status)
  - `ServiceRecord`: historical details for maintenance logs (extensible)

Request lifecycle example (Customer booking):
- GET `/services/book/` → show `BookServiceForm`
- POST → validate, create `Service(customer=request.user, status=pending)` → redirect to dashboard

Extendability:
- Add invoicing models related to `Service`
- Notifications on status change
- Replace SQLite with Postgres in production
