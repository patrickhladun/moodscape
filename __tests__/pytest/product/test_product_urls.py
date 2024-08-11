import pytest

from django.urls import URLPattern, URLResolver, reverse, resolve
from django.test import Client

from apps.product.urls import urlpatterns
from apps.product import views


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
def test_product_url_resolves(test_data_products):
    client = Client()

    product = test_data_products[0]
    url = reverse("product", args=[product.slug])
    resolver = resolve(url)
           
    assert resolver.view_name == 'product'
    assert resolver.func == views.product_view
    assert resolver.kwargs['slug'] == product.slug