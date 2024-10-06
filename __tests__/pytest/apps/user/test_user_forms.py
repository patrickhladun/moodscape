import pytest

from __tests__.pytest.factories import SuperuserFactory
from apps.user.forms import AccountProfileForm


@pytest.mark.django_db
def test_account_form_initial_state():
    form = AccountProfileForm()
    assert not form.is_bound


@pytest.mark.django_db
def test_account_form_update_email():
    superuser = SuperuserFactory()

    form_data = {
        "email": "newemail@example.com",
        "username": superuser.username,
    }
    form = AccountProfileForm(data=form_data, instance=superuser)

    assert form.is_valid()
    updated_user = form.save()
    assert updated_user.email == "newemail@example.com"


@pytest.mark.django_db
def test_account_form_update_username():
    superuser = SuperuserFactory()

    form_data = {
        "email": superuser.email,
        "username": "newusername",
    }
    form = AccountProfileForm(data=form_data, instance=superuser)

    assert form.is_valid()
    updated_user = form.save()
    assert updated_user.username == "newusername"


@pytest.mark.django_db
def test_account_form_missing_email():
    superuser = SuperuserFactory()

    form_data = {
        "email": "",
        "username": superuser.username,
    }
    form = AccountProfileForm(data=form_data, instance=superuser)

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_account_form_invalid_email():
    superuser = SuperuserFactory()

    form_data = {
        "email": "invalid-email",
        "username": superuser.username,
    }
    form = AccountProfileForm(data=form_data, instance=superuser)

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_account_form_missing_username():
    superuser = SuperuserFactory()

    form_data = {
        "email": superuser.email,
        "username": "",
    }
    form = AccountProfileForm(data=form_data, instance=superuser)

    assert not form.is_valid()
    assert "username" in form.errors
