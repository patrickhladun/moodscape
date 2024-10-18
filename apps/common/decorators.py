from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def check_superuser(user):
    return user.is_superuser


def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser,
    redirects to the login page if necessary.
    """

    def view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_url")
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return login_required(view)
