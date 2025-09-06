# Templates

Base Layout
- `services/base.html` loads Bootstrap, navbar, and defines `{% block content %}`.

Auth Templates
- `services/login.html`, `services/signup.html` extend base and use Bootstrap classes.

Dashboards
- `services/dashboards/customer.html`
- `services/dashboards/mechanic.html`
- `services/dashboards/manager.html`

Service Actions
- `services/services_book.html`
- `services/services_assign.html`
- `services/services_update_status.html`

Tip: Always extend `services/base.html` to ensure consistent styling.
