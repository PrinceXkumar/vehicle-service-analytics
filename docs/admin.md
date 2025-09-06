# Admin

Registered models:
- `Profile` with list display (user, role, phone, created_at)
- `Vehicle`
- `ServiceRecord`
- `Service` with filters and autocomplete

User Inline Profile:
- The default `User` admin is unregistered and re-registered with a `ProfileInline`.
- Lets you manage role/phone/address alongside the user.

Tips:
- Use search and list filters for quick lookups.
- Create a superuser via `createsuperuser` to access `/admin`.
