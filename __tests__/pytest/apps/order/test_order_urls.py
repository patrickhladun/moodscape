import pytest
from django.test import Client
from django.urls import URLPattern, URLResolver, resolve, reverse

from __tests__.pytest.factories import SuperuserFactory
from apps.order import views
from apps.order.urls import urlpatterns


@pytest.mark.django_db
def test_no_empty_path():
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            assert pattern.pattern._route != "", "Empty path pattern found!"
        elif isinstance(pattern, URLResolver):
            # Recursively check included URL configurations
            for sub_pattern in pattern.url_patterns:
                assert (
                    sub_pattern.pattern._route != ""
                ), "Empty path pattern found in included urls!"


@pytest.mark.django_db
def test_cms_orders_url_resolves():
    expected_url = f"/cms/orders/"

    url = reverse("cms_orders")
    resolver = resolve(url)

    assert resolver.view_name == "cms_orders"
    assert resolver.func == views.cms_orders_view
    assert url == expected_url


@pytest.mark.django_db
def test_cms_order_update_url_resolves():
    order_number = "HDY36872GED"
    expected_url = f"/cms/orders/{order_number}/update/"

    url = reverse("cms_order_update", args=[order_number])
    resolver = resolve(url)

    assert resolver.kwargs["order_number"] == order_number
    assert resolver.view_name == "cms_order_update"
    assert resolver.func == views.cms_order_update_view
    assert url == expected_url
