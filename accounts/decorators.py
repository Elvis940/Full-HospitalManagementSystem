from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    """Require user to have one of the specified roles"""
    def check_role(user):
        if user.is_authenticated:
            if user.role in roles or user.is_superuser:
                return True
        raise PermissionDenied
    return user_passes_test(check_role)