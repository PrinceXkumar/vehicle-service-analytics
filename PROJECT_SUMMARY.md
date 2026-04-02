# Project Summary: AutoInsight

This document provides an overview of the **AutoInsight** project, detailing each file's purpose and the features implemented throughout the development process.

## Project Overview
The AutoInsight application is a Django-based platform designed to manage vehicle service workflows. It features a robust **Role-Based Access Control (RBAC)** system for Customers, Mechanics, and Managers, each with their own specialized dashboards and analytics insights.

## Directory Structure
```text
vehicle_service_analytics/
├── manage.py                   # Django management CLI
├── db.sqlite3                  # Development database
├── requirements.txt            # Project dependencies
├── vehicle_service_analytics/   # Project configuration
│   ├── settings.py             # Global settings (DB, Auth, Middleware)
│   ├── urls.py                 # Global URL routing
│   ├── asgi.py & wsgi.py       # Deployment interfaces
└── services/                   # Main application app
    ├── models.py               # Data models (Profile, Service, Vehicle)
    ├── views.py                # Request handling & business logic
    ├── forms.py                # UI-ready forms (Signup, Booking, etc.)
    ├── urls.py                 # App-specific routing
    ├── admin.py                # Admin interface customization
    ├── signals.py              # Automatic Profile creation logic
    ├── analytics.py            # Analytics calculation engine
    ├── decorators.py           # Custom access control decorators
    ├── management/commands/    # CLI tools (sample data generation)
    └── templates/services/     # HTML templates (Dashboards, Analytics)
```

---

## File-by-File Breakdown

### 1. `manage.py`
A standard Django management script used to interact with the project (e.g., `runserver`, `migrate`, `createsuperuser`).

### 2. `vehicle_service_analytics/settings.py`
The configuration hub of the project. Key configurations include:
- **Authentication**: Integrated with `services.apps.ServicesConfig`.
- **Database**: SQLite for development, with ready-to-use PostgreSQL support for production.
- **Middleware**: Includes WhiteNoise for static file serving in production.
- **Redirects**: Defines `LOGIN_REDIRECT_URL = 'dashboard'` to route users correctly after login.

### 3. `services/models.py`
Defines the core data structures:
- **Profile**: Extends the base `User` model to include roles (`Customer`, `Mechanic`, `Manager`), phone numbers, and addresses.
- **Vehicle**: Stores vehicle details (Make, Model, VIN, Mileage) linked to a `User`.
- **Service**: Tracks service bookings, types (`Oil Change`, etc.), statuses (`Pending`, `Completed`), and the assigned mechanic.
- **ServiceRecord**: Historically tracks completed services with costs and work details.

### 4. `services/views.py`
Handles all application logic and rendering:
- **Auth**: `signup_view` handles user registration and role assignment.
- **Dashboards**: Separate views for `dashboard_customer`, `dashboard_mechanic`, and `dashboard_manager`.
- **Workflows**: `book_service` (Customer), `assign_mechanic` (Manager), and `update_service_status` (Mechanic).
- **Analytics**: Dedicated views for data visualization and report exports.

### 5. `services/analytics.py`
The "brain" behind the charts and reports:
- **ServiceAnalytics**: Aggregates data for trend analysis, status distribution, and mechanic performance.
- **ReportGenerator**: Includes logic to export data into **CSV** and **Excel** formats using `openpyxl`.

### 6. `services/forms.py`
Custom forms styled with Bootstrap:
- **SignUpForm**: Captures extended profile details beyond standard Django user fields.
- **BookServiceForm**, **AssignMechanicForm**, **UpdateStatusForm**: Streamlined inputs for the service workflow.

### 7. `services/signals.py`
Automates background tasks. Specifically, it uses `post_save` signals to ensure every `User` has a corresponding `Profile` upon creation.

### 8. `services/decorators.py`
Provides `role_required`, a custom decorator that enforces access control based on the user's role defined in their profile.

---

## What You Have Accomplished

### Part 1: Core Infrastructure
- Initialized the Django project and `services` app.
- Set up base routing and a clean repository structure.

### Part 2: Authentication & UI
- Integrated **Bootstrap 5** for a modern look.
- Implemented Login, Signup, and Logout workflows with custom-styled templates.

### Part 3: Identity & Roles
- Developed the `Profile` system to support different user roles.
- Linked profile creation to user registration using Django Signals.

### Part 4: Role-Based Dashboards
- Built distinct dashboards for each user type.
- Implemented smart redirection based on user identity.

### Part 5: Service Workflows
- Created the `Service` model and booking system.
- Enabled Managers to assign jobs and Mechanics to update progress.
- Enhanced the Django Admin to manage everything in one place.

### Part 6: Analytics & Reporting
- Integrated **Chart.js** for interactive data visualization.
- Built a comprehensive reporting system with CSV/Excel exports.
- Developed a CLI command (`populate_sample_data`) to test the system at scale.
