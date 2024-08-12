import pytest

from django.test import Client
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.frontend import views
from apps.product.models import Product, Category


@pytest.mark.django_db
def test_product_view(test_data_products):
    client = Client()

    product = test_data_products[0]
    response = client.get(reverse("product", args=[product.slug]))
    
    assert response.status_code == 200
    assert "product/product.html" in (t.name for t in response.templates)

    product = get_object_or_404(Product, slug=product.slug)

    assert response.context["product"].name == "Irish Coastal Sunset Watercolor"
    assert response.context["product"].slug == "irish-coastal-sunset-watercolor"
    assert response.context["product"].details == ""
    assert response.context["product"].sku == "wtc-ol-icsw1"
    assert response.context["product"].stock == 10
    assert response.context["product"].price == 128
    assert response.context["product"].featured == "products/irish-coastal-sunset-watercolor.webp"
    assert response.context["product"].category.name == "Watercolor"
    assert response.context["product"].is_draft == False