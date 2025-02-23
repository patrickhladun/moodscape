import pytest
from django.urls import resolve

from apps.frontend import views

urls = [
    {
        "url": "/",
        "name": "home",
    },
    {
        "url": "/about/",
        "name": "about",
    },
    {
        "url": "/contact/",
        "name": "contact",
    },
    {
        "url": "/contact/success/",
        "name": "success_contact",
    },
    {
        "url": "/privacy-policy/",
        "name": "privacy",
    },
    {
        "url": "/terms-and-conditions/",
        "name": "terms",
    },
    {
        "url": "/faq/",
        "name": "faq",
    },
    {
        "url": "/shop/",
        "name": "shop",
    },
]


@pytest.mark.parametrize("url", urls)
def test_urls_resolves(url):
    resolver = resolve(url["url"])
    assert resolver.view_name == url["name"]
    assert resolver.func == getattr(views, url["name"])
