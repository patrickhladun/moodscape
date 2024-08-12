import pytest

from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model

from apps.user.admin import UserAdmin

User = get_user_model()

@pytest.mark.django_db
def test_user_admin_registration():
    assert site._registry[User].__class__ == UserAdmin


@pytest.mark.django_db
def test_user_admin_list_display():
    user_admin = site._registry[User]
    assert user_admin.list_display == ('email', 'username', 'is_superuser', 'is_staff', 'is_active', 'user_type', 'date_joined', 'last_login')


@pytest.mark.django_db
def test_user_admin_search_fields():
    user_admin = site._registry[User]
    assert user_admin.search_fields == ('email', 'username')


@pytest.mark.django_db
def test_user_admin_ordering():
    user_admin = site._registry[User]
    assert user_admin.ordering == ('email',)


@pytest.mark.django_db
def test_user_admin_fieldsets():
    user_admin = site._registry[User]
    assert user_admin.fieldsets == (
        (None, {'fields': ('email', 'username', 'password', 'last_login', 'date_joined', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
    )


@pytest.mark.django_db
def test_user_admin_add_fieldsets():
    user_admin = site._registry[User]
    assert user_admin.add_fieldsets == (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )


@pytest.mark.django_db
def test_user_admin_readonly_fields():
    user_admin = site._registry[User]
    assert user_admin.readonly_fields == ('last_login', 'date_joined')
