# Forms

## SignUpForm
- Extends `UserCreationForm`
- Adds: `full_name`, `phone`, `address`, `role`
- Styles fields in `__init__` with Bootstrap classes
- Splits full name into first/last in the signup view

## BookServiceForm
- ModelForm for `Service`
- Field: `service_type`

## AssignMechanicForm
- ModelForm for `Service`
- Field: `assigned_mechanic`
- Queryset filtered to users with role = Mechanic

## UpdateServiceStatusForm
- ModelForm for `Service`
- Field: `status`
