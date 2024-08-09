import pytest
from django.conf import settings
from django.urls import reverse
from apps.user.forms import AccountProfileForm
from __tests__.pytest.factories import SuperuserFactory

views = [
    {
        'url': 'user_account',
        'template': 'user/admin/account.html',
    },
]

@pytest.mark.parametrize("view", views)
def test_view_status_for_unauthenticated_user(client, view):
    url = reverse(view['url'])
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize("view", views)
def test_view_status_for_authenticated_user(client, view):
    superuser = SuperuserFactory()

    superuser = SuperuserFactory()
    superuser.set_password("4KDo#YFz3QG&6LIBh$")
    superuser.save()

    client.force_login(superuser)

    url = reverse(view['url'])
    response = client.get(url)
    
    assert response.status_code == 200
    assert view['template'] in [t.name for t in response.templates]


@pytest.mark.django_db
def test_account_view_form(client):
    superuser = SuperuserFactory()

    superuser = SuperuserFactory()
    superuser.set_password("19IY4YOOV9BEOUWyjM")
    superuser.save()

    client.force_login(superuser)

    response = client.get(reverse("user_account"))
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, AccountProfileForm)
    assert str(form.instance.pk) == str(superuser.pk)


@pytest.mark.django_db
def test_update_user_email_form(client):
    superuser = SuperuserFactory()

    superuser = SuperuserFactory()
    superuser.set_password("fFJalbGV!Ot78cRk0b")
    superuser.save()

    client.force_login(superuser)

    response = client.get(reverse("user_account"))
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, AccountProfileForm)
    assert str(form.instance.pk) == str(superuser.pk)

    new_email = "newemail@example.com"
    form_data = {
        "email": new_email,
        "username": superuser.username,
    }

    # Submit the form via POST request
    response = client.post(reverse("user_account"), data=form_data)

    assert response.status_code == 302

    response = client.get(reverse("user_account"))
    assert response.status_code == 200

    superuser.refresh_from_db()
    assert superuser.email == new_email