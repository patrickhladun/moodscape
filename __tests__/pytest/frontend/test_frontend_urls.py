import pytest
from django.urls import resolve
from apps.frontend import views

urls = [
    {
        'url': '/',
        'name': 'home',
    },
    {
        'url': '/about/',
        'name': 'about',
    },
    {
        'url': '/contact/',
        'name': 'contact',
    },
    {
        'url': '/contact/success/',
        'name': 'contact_success',
    },
    {
        'url': '/privacy-policy/',
        'name': 'privacy',
    },
]

@pytest.mark.parametrize("url", urls)
def test_urls_resolves(url):
    resolver = resolve(url['url'])
    assert resolver.view_name == url['name']
    assert resolver.func == getattr(views, url['name'])