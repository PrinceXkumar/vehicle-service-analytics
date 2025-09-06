# Vehicle Service Analytics

A Django web app for managing vehicle service workflows with role-based dashboards for Customers, Mechanics, and Managers.

- Repo: https://github.com/PrinceXkumar/vehicle-service-analytics

## Tech Stack
- Django 5
- SQLite (dev)
- Bootstrap 5 (CDN)

## Features
- Authentication (login, logout, signup)
- Profiles with roles: Customer, Mechanic, Manager
- Role-based dashboards and access control
- Service booking (Customer)
- Job assignment (Manager)
- Status updates (Mechanic)
- Django Admin: Users, Profiles (inline), Services
- **Analytics & Reporting System**:
  - Manager Analytics: Interactive charts (bar, pie, doughnut) for service trends, status distribution, top performers
  - Customer Analytics: Personal service history with line charts and yearly tracking
  - Mechanic Analytics: Performance metrics, completion rates, and job distribution
  - Export functionality: CSV/Excel reports with filtering options
  - Sample data generation for testing

## Getting Started
1) Create and activate a virtualenv (Windows example)
```
python -m venv venv
./venv/Scripts/activate
```

2) Install requirements
```
pip install django djangorestframework
```

3) Apply migrations and run
```
./venv/Scripts/python.exe manage.py makemigrations
./venv/Scripts/python.exe manage.py migrate
./venv/Scripts/python.exe manage.py runserver
```

4) Create superuser (for Admin)
```
./venv/Scripts/python.exe manage.py createsuperuser
```

5) Generate sample data for testing analytics (optional)
```
./venv/Scripts/python.exe manage.py populate_sample_data --count 30
```

## Usage Overview
- Signup at `/signup` (choose role)
- Login at `/login`
- After login you are redirected to `/dashboard` which routes to:
  - Customer: `/dashboard/customer/`
  - Mechanic: `/dashboard/mechanic/`
  - Manager: `/dashboard/manager/`
- **Analytics dashboards** available at `/analytics/` (role-based routing):
  - Manager: `/analytics/manager/` - Comprehensive analytics with charts
  - Customer: `/analytics/customer/` - Personal service history
  - Mechanic: `/analytics/mechanic/` - Performance metrics

### Customer
- Book a service: `/services/book/`
- See recent bookings on dashboard

### Manager
- See totals (dynamic) and pending list
- Assign mechanic: `/services/<id>/assign/`

### Mechanic
- See assigned jobs
- Update status: `/services/<id>/status/`

## Admin
- Visit `/admin`
- Users have Profile inline (role, phone, address)
- Manage `Service` entries (filters, search, autocomplete)

## Data Model (Core)
- `Profile`: `user`, `role`, `phone`, `address`, `created_at`
- `Service`:
  - `customer` (FK to User)
  - `service_type` (Oil Change, Tyre Replacement, Brake Inspection, General Checkup)
  - `status` (Pending, In Progress, Completed)
  - `assigned_mechanic` (FK to User, optional)
  - `created_at`

Note: A historical `ServiceRecord` model also exists for extended service details; it’s currently independent of `Service`.

## Access Control
- `LOGIN_REDIRECT_URL = 'dashboard'`
- `role_required([...])` decorator ensures only allowed roles can access each dashboard/action.

## Project Roadmap
- Charts for Manager analytics (Chart.js/Matplotlib)
- Customer service history details and invoices
- Mechanic work logs and time tracking
- Email/SMS notifications



## Part-by-Part Changelog
- Part 1: Initial Django project setup and base pages
  - Project scaffolding, base URLs, home page, basic templates
- Part 2: Added Bootstrap to base, login, signup, logout
  - Styled `base.html`, `login.html`, `signup.html`, improved layout
- Part 3: Added Profile model with roles (Customer, Mechanic, Manager)
  - `Profile` model + signals, signup extended to capture role/phone/address
- Part 4: Implemented role-based dashboards
  - Redirect after login, dashboards per role with access control
- Part 5: Added Service model + Admin integration
  - Booking (Customer), Assigning (Manager), Status updates (Mechanic), dynamic dashboards, Admin registration

## Repository Hygiene
- `.gitignore` excludes: venv, SQLite DBs, caches, IDE files, static build

## License
MIT

---

## Project Structure
```
vehicle_service_analytics/
├─ manage.py
├─ vehicle_service_analytics/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
└─ services/
   ├─ models.py          # Profile, Vehicle, ServiceRecord, Service
   ├─ views.py           # Auth, dashboards, booking/assign/update flows, analytics
   ├─ urls.py
   ├─ forms.py           # SignUp, BookService, AssignMechanic, UpdateStatus
   ├─ admin.py           # User inline Profile, Service admin
   ├─ signals.py         # Auto-create Profile on User create
   ├─ analytics.py       # Analytics engine and report generation
   ├─ management/commands/
   │  └─ populate_sample_data.py  # Sample data generation
   └─ templates/services/
      ├─ base.html
      ├─ login.html
      ├─ signup.html
      ├─ dashboards/
      │  ├─ customer.html
      │  ├─ mechanic.html
      │  └─ manager.html
      ├─ analytics/
      │  ├─ manager_analytics.html
      │  ├─ customer_analytics.html
      │  └─ mechanic_analytics.html
      ├─ services_book.html
      ├─ services_assign.html
      └─ services_update_status.html
```

## Environment & Configuration
- No external environment variables required for development.
- Default DB: SQLite file `db.sqlite3` (auto-created).
- Static files served via Bootstrap CDN; no local static build needed for dev.

## Creating Demo Users (optional)
Run from Django shell to quickly create users of each role:
```
./venv/Scripts/python.exe manage.py shell
```
```python
from django.contrib.auth.models import User
from services.models import Profile

def create_user(u, p, r, fn):
    user, _ = User.objects.get_or_create(username=u, defaults={"email": f"{u}@example.com"})
    user.set_password(p); user.first_name = fn; user.save()
    prof, _ = Profile.objects.get_or_create(user=user); prof.role = r; prof.save()
    print(u, r)

create_user('alice', 'pass12345', Profile.ROLE_CUSTOMER, 'Alice')
create_user('mike', 'pass12345', Profile.ROLE_MECHANIC, 'Mike')
create_user('maria', 'pass12345', Profile.ROLE_MANAGER, 'Maria')
```

## Part-wise Commit Commands
Use these to create clean history (adjust paths if needed):
```
git init
git add .gitignore manage.py vehicle_service_analytics/**/* services/apps.py services/urls.py services/templates/services/home.html
git commit -m "Part 1: Initial Django project setup and base pages"

git add services/templates/services/base.html services/templates/services/login.html services/templates/services/signup.html
git commit -m "Part 2: Added Bootstrap to base, login, signup, logout"

git add services/models.py services/signals.py services/forms.py services/views.py vehicle_service_analytics/settings.py
git commit -m "Part 3: Added Profile model with roles (Customer, Mechanic, Manager)"

git add services/decorators.py services/views.py services/urls.py services/templates/services/dashboards/* services/templates/services/base.html vehicle_service_analytics/settings.py
git commit -m "Part 4: Implemented role-based dashboards"

git add services/models.py services/forms.py services/views.py services/urls.py services/templates/services/services_* services/templates/services/dashboards/* services/admin.py
git commit -m "Part 5: Added Service model + Admin integration"

git branch -M main
git remote add origin https://github.com/PrinceXkumar/vehicle-service-analytics.git
git push -u origin main
```

## Common Commands
```
./venv/Scripts/python.exe manage.py makemigrations
./venv/Scripts/python.exe manage.py migrate
./venv/Scripts/python.exe manage.py runserver
./venv/Scripts/python.exe manage.py createsuperuser
```

## Troubleshooting
- TemplateDoesNotExist: ensure templates extend `services/base.html` and paths match.
- Profile missing on login: make sure `services.apps.ServicesConfig` is in `INSTALLED_APPS` so signals load.
- Access denied: check the user’s `Profile.role` and use the right dashboard URL.

## Detailed Part History (Past-wise Information)
This section documents what changed in each part, with intended commit messages and key files.

### Part 1 — Initial Setup & Base Pages
- Commit: "Part 1: Initial Django project setup and base pages"
- Highlights:
  - Created Django project and `services` app
  - Basic routing in `vehicle_service_analytics/urls.py` and `services/urls.py`
  - Minimal home template
- Key files: `manage.py`, `vehicle_service_analytics/settings.py`, `vehicle_service_analytics/urls.py`, `services/urls.py`, `services/templates/services/home.html`, `.gitignore`

### Part 2 — Bootstrap + Auth Screens
- Commit: "Part 2: Added Bootstrap to base, login, signup, logout"
- Highlights:
  - Styled layout in `services/templates/services/base.html`
  - Login and Signup templates styled with Bootstrap
  - Auth routes wired (`login`, `logout`, `signup`)
- Key files: `services/templates/services/base.html`, `services/templates/services/login.html`, `services/templates/services/signup.html`

### Part 3 — Profiles & Extended Signup
- Commit: "Part 3: Added Profile model with roles (Customer, Mechanic, Manager)"
- Highlights:
  - `Profile` model with roles, phone, address
  - Signals to auto-create `Profile` on `User` create
  - Signup form captures role, phone, address; splits full name
  - Ensured `ServicesConfig` is used in `INSTALLED_APPS`
- Key files: `services/models.py`, `services/signals.py`, `services/forms.py`, `services/views.py`, `vehicle_service_analytics/settings.py`

### Part 4 — Role-based Dashboards
- Commit: "Part 4: Implemented role-based dashboards"
- Highlights:
  - Dashboard redirect after login based on role
  - Customer, Mechanic, Manager dashboards with access control
  - Navbar link to Dashboard
- Key files: `services/decorators.py`, `services/views.py`, `services/urls.py`, `services/templates/services/dashboards/*.html`, `services/templates/services/base.html`, `vehicle_service_analytics/settings.py`

### Part 5 — Service Model & Workflows
- Commit: "Part 5: Added Service model + Admin integration"
- Highlights:
  - `Service` model (customer, service_type, status, assigned_mechanic)
  - Booking form (Customer), Assign mechanic (Manager), Update status (Mechanic)
  - Dashboards now dynamic (totals, lists)
  - Admin for `Service` and inline `Profile` on `User`
- Key files: `services/models.py`, `services/forms.py`, `services/views.py`, `services/urls.py`, `services/templates/services/services_*.html`, `services/templates/services/dashboards/*.html`, `services/admin.py`

### Part 6 — Analytics & Reporting System
- Commit: "Added Part 6: Analytics dashboard with charts and reports"
- Highlights:
  - **Manager Analytics Dashboard** (`/analytics/manager/`):
    - Interactive charts using Chart.js (bar, pie, doughnut charts)
    - Monthly service trends, status distribution, service type breakdown
    - Top performers table and most popular service types
    - Export functionality (CSV/Excel) with filtering options
  - **Customer Analytics Dashboard** (`/analytics/customer/`):
    - Personal service history with line charts
    - Service status overview and quick actions
    - Yearly service tracking and insights
  - **Mechanic Analytics Dashboard** (`/analytics/mechanic/`):
    - Performance metrics and completion rates
    - Job status distribution with visual charts
    - Monthly performance insights and progress tracking
  - **Export System** (`/analytics/export/`):
    - CSV and Excel report generation
    - Status-based filtering (all, pending, completed, in_progress)
    - Professional report formatting
  - **Sample Data Generation**:
    - Management command `populate_sample_data` for testing
    - Realistic test data with proper distributions
- Key files: `services/analytics.py`, `services/views.py` (analytics views), `services/templates/services/analytics/*.html`, `services/management/commands/populate_sample_data.py`, `services/urls.py` (analytics routes)
- Technologies: Chart.js, Django ORM aggregations, CSV/Excel export, Bootstrap 5