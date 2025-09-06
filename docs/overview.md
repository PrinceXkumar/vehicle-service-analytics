# Overview

This project is a learning-friendly Vehicle Service Management app built with Django.

Goals:
- Show role-based access with real user flows
- Demonstrate clean separation of models, forms, views, and templates
- Keep code readable and extendable

Main modules:
- `services/models.py`: data schema (Profile, Vehicle, ServiceRecord, Service)
- `services/forms.py`: validated user input (signup, booking, assigning, status updates)
- `services/views.py`: controllers that handle requests and return responses
- `services/urls.py`: routes URLs to views
- `services/templates/`: UI templates (base, auth, dashboards, service actions)
- `services/signals.py`: connect Django signals (auto create Profile)
- `services/admin.py`: admin site configuration

Start by reading Architecture & Flow next.
