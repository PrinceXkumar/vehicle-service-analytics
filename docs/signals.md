# Signals

`services/signals.py`
- Listens to `post_save` on `User`.
- On create: `Profile.objects.create(user=instance)`
- On update: ensures a Profile exists and saves it.

Why?
- Guarantees every user has a Profile without manual steps.

Ensure `services.apps.ServicesConfig` is in `INSTALLED_APPS` so `ready()` imports signals.
