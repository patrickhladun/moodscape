import pytest

from django.urls import URLPattern, URLResolver, reverse, resolve
from django.test import Client

from __tests__.pytest.factories import SuperuserFactory

from apps.order.urls import urlpatterns
from apps.order import views


@pytest.mark.django_db
def test_no_empty_path():
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            assert pattern.pattern._route != "", "Empty path pattern found!"
        elif isinstance(pattern, URLResolver):
            # Recursively check included URL configurations
            for sub_pattern in pattern.url_patterns:
                assert sub_pattern.pattern._route != "", "Empty path pattern found in included urls!"


@pytest.mark.django_db
def test_orders_url_resolves():
    expected_url = f"/account/orders/"

    url = reverse("admin_orders")
    resolver = resolve(url)

    assert resolver.view_name == 'admin_orders'
    assert resolver.func == views.orders_view
    assert url == expected_url


@pytest.mark.django_db
def test_order_update_url_resolves():
    order_number = "HDY36872GED"
    expected_url = f"/account/orders/{order_number}/update/"
    
    url = reverse("admin_order_update", args=[order_number])
    resolver = resolve(url)
    
    assert resolver.kwargs['order_number'] == order_number
    assert resolver.view_name == 'admin_order_update'
    assert resolver.func == views.order_update_view
    assert url == expected_url


