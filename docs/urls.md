# URLs & Routing

`services/urls.py`:
- `/login/` → Django auth LoginView
- `/logout/` → Django auth LogoutView
- `/signup/` → `signup_view`
- `/dashboard/` → `dashboard_redirect`
- `/dashboard/customer/` → `dashboard_customer`
- `/dashboard/mechanic/` → `dashboard_mechanic`
- `/dashboard/manager/` → `dashboard_manager`
- `/services/book/` → `book_service`
- `/services/<id>/assign/` → `assign_mechanic`
- `/services/<id>/status/` → `update_service_status`

Project URLs include `services.urls` at the root.
