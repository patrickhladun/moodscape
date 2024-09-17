import pytest

from django.urls import reverse
from django.conf import settings

from apps.user.forms import AccountProfileForm
from __tests__.pytest.factories import UserFactory, SuperuserFactory

views = [
    {
        'url': 'account',
        'template': 'user/account/account.html',
    },
]

@pytest.mark.parametrize("view", views)
def test_view_status_for_unauthenticated_user(client, view):
    url = reverse(view['url'])
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize("view", views)
def test_view_status_for_authenticated_account_user(client, view):
    account = UserFactory()
    account.set_password("4KDo#YFz3QG&6LIBh$")
    account.save()

    client.force_login(account)

    url = reverse(view['url'])
    response = client.get(url)
    
    assert response.status_code == 200
    assert view['template'] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_account_view_form(client):
    account = UserFactory()
    account.set_password("19IY4YOOV9BEOUWyjM")
    account.save()

    client.force_login(account)

    response = client.get(reverse("account"))
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, AccountProfileForm)
    assert str(form.instance.pk) == str(account.pk)


@pytest.mark.django_db
def test_update_account_user_email_form(client):
    account = UserFactory()
    account.set_password("19IY4YOOV9BEOUWyjM")
    account.save()

    client.force_login(account)

    response = client.get(reverse("account"))
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, AccountProfileForm)
    assert str(form.instance.pk) == str(account.pk)

    new_email = "newemail@example.com"
    form_data = {
        "email": new_email,
        "username": account.username,
    }

    response = client.post(reverse("account"), data=form_data)

    assert response.status_code == 302

    response = client.get(reverse("account"))
    assert response.status_code == 200

    account.refresh_from_db()
    assert account.email == new_email