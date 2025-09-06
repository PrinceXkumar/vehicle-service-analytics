# Models

## Profile
- OneToOne with `User`
- Fields: `role`, `phone`, `address`, `created_at`
- Purpose: extend the built-in user with application-specific attributes

## Vehicle
- Belongs to a `User` (owner)
- Basic attributes (make, model, year, vin, registration_number)
- Purpose: support future linking with service history

## ServiceRecord
- Linked to a `Vehicle`
- Historical maintenance info: date, odometer, costs
- Purpose: long-term record keeping (reports/analytics)

## Service
- Core operational workflow entity
- Fields:
  - `customer` (User)
  - `service_type` (choices: oil change, tyre replacement, etc.)
  - `status` (pending, in_progress, completed)
  - `assigned_mechanic` (User, optional)
  - `created_at`
- Purpose: booking → assignment → status updates
