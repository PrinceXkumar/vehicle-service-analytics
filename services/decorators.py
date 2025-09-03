from functools import wraps
from django.http import HttpResponseForbidden


def role_required(allowed_roles):
    """Allow access only if request.user.profile.role is in allowed_roles."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                # Let login_required handle unauthenticated cases if applied
                return HttpResponseForbidden("Permission Denied")
            profile = getattr(user, "profile", None)
            if profile and profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Permission Denied")
        return _wrapped
    return decorator


