import pytest

from django.test import Client
from django.urls import reverse
from django.conf import settings

from apps.frontend.forms import ContactForm

views = [
    {
        'url': 'home',
        'template': 'frontend/index.html',
    },
    {
        'url': 'about',
        'template': 'frontend/about.html',
    },
    {
        'url': 'contact',
        'template': 'frontend/contact.html',
    },
    {
        'url': 'success_contact',
        'template': 'frontend/success_contact.html',
    },
    {
        'url': 'privacy',
        'template': 'frontend/privacy.html',
    },
    {
        'url': 'terms',
        'template': 'frontend/terms.html',
    },
    {
        'url': 'faq',
        'template': 'frontend/faq.html',
    },
    {
        'url': 'shop',
        'template': 'frontend/shop.html',
    },
]

@pytest.mark.django_db
@pytest.mark.parametrize("view", views)
def test_views_status(client, view):
    url = reverse(view['url'])
    response = client.get(url)

    assert response.status_code == 200
    assert view['template'] in [t.name for t in response.templates]

@pytest.mark.django_db
def test_contact_form_initial_state(client):
    response = client.get(reverse('contact'))
    form = response.context['form']
    assert not form.is_bound

@pytest.mark.django_db
def test_contact_post_valid(client, mailoutbox):
    url = reverse('contact')
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'This is a test message.'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('success_contact')

    assert len(mailoutbox) == 1
    email = mailoutbox[0]
    assert email.to == ['john@example.com']
    assert email.subject == "Thank you for contacting Moodscape"
    assert settings.DEFAULT_FROM_EMAIL in email.from_email

    email_body = "Dear John Doe!\n\nThank you for reaching out! We have " \
    "received your message and will get back to you soon.\n\nHere is your " \
    "email:\nThis is a test message.\n\nMoodscape Team\n"

    assert email_body == email.body


@pytest.mark.django_db
def test_contact_post_invalid(client):
    url = reverse('contact')
    data = {
        'name': '',
        'email': 'john@example.com',
        'message': 'This is a test message.'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ContactForm)
    assert response.context['form'].errors
    assert 'frontend/contact.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_shop_view_list_all_products(test_data_products):
    client = Client()

    response = client.get(reverse('shop'))

    assert response.status_code == 200
    assert 'frontend/shop.html' in [t.name for t in response.templates]
    assert len(response.context["products"]) == 8

    assert response.context["products"][0].name == "Original Watercolor Seascape Abstract Painting, Wall Art Abstract Art Purple."
    assert response.context["products"][0].slug == "irish-watercolor-seascape-abstract"
    assert response.context["products"][0].sku == "wtc-ol-owsa1"
