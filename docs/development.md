# Development Guide

Dev tasks
- Run server: `./venv/Scripts/python.exe manage.py runserver`
- Make migrations: `./venv/Scripts/python.exe manage.py makemigrations`
- Migrate: `./venv/Scripts/python.exe manage.py migrate`
- Admin: `./venv/Scripts/python.exe manage.py createsuperuser`

Testing ideas
- Unit tests for views and forms
- Factory data for Services per role

Extending next
- Replace SQLite with Postgres
- Add charts for manager analytics
- Email/SMS notifications on status changes
- Service invoice model and PDF export
