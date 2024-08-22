from django.contrib.auth.decorators import user_passes_test


def check_superuser(user):
    return user.is_superuser


def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser,
    redirects to the login page if necessary.
    """
    decorated_view_func = user_passes_test(check_superuser)(view_func)
    return decorated_view_func
