import pytest
from django.urls import resolve

from apps.user import views

urls = [{"url": "/account/", "name": "account", "view": views.account_view}]


@pytest.mark.parametrize("url_data", urls)
def test_urls_resolve(url_data):
    resolver = resolve(url_data["url"])
    assert resolver.view_name == url_data["name"]
    assert resolver.func == url_data["view"]
