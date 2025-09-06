# Access Control & Roles

- `LOGIN_REDIRECT_URL = 'dashboard'` directs to a role-aware redirect view after login.
- `role_required(allowed_roles)` decorator blocks access for mismatched roles.
- Combine with `login_required` to ensure authenticated access only.

Example:
```python
@login_required
@role_required([Profile.ROLE_MANAGER])
def dashboard_manager(request):
    ...
```

Why?
- Prevents a customer from visiting manager routes, and vice versa.
- Keeps the UI and permissions consistent.
