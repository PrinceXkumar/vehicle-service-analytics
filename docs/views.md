# Views

## Auth & Home
- `home`: simple landing page
- `signup_view`: handles signup, sets email, splits full name, ensures Profile

## Dashboards
- `dashboard_redirect`: routes by `Profile.role`
- `dashboard_customer`: recent bookings list
- `dashboard_manager`: totals + pending list
- `dashboard_mechanic`: assigned jobs list

## Service Workflow
- `book_service`: create Service (customer)
- `assign_mechanic`: set assigned_mechanic (manager)
- `update_service_status`: change status (mechanic)

All dashboard/service views are protected with `login_required` and `role_required` as appropriate.
