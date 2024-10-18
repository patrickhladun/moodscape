import pytest
from django.contrib.admin.sites import site
from django.urls import reverse
from django.utils.safestring import SafeString

from apps.product.admin import CategoryAdmin, ProductAdmin
from apps.product.models import Category, Product


@pytest.mark.django_db
def test_category_admin_registration():
    assert site._registry[Category].__class__ == CategoryAdmin


@pytest.mark.django_db
def test_category_admin_list_display():
    category_admin = site._registry[Category]
    assert category_admin.list_display == ("name", "slug")


@pytest.mark.django_db
def test_product_admin_registration():
    assert site._registry[Product].__class__ == ProductAdmin


@pytest.mark.django_db
def test_product_admin_list_display():
    product_admin = site._registry[Product]
    assert product_admin.list_display == (
        "display_featured",
        "product_name",
        "sku",
        "price",
        "category",
        "created_at",
        "updated_at",
        "is_published",
    )


@pytest.mark.django_db
def test_product_admin_display_featured(test_data_products):
    product_admin = site._registry[Product]
    product = test_data_products[0]

    featured_html = product_admin.display_featured(product)
    assert isinstance(featured_html, SafeString)
    assert "img" in featured_html

    product.featured = None
    default_image_html = product_admin.display_featured(product)
    assert isinstance(default_image_html, SafeString)
    assert "img" in default_image_html
    assert "avatar.png" in default_image_html


@pytest.mark.django_db
def test_product_admin_product_name(test_data_products):
    product_admin = site._registry[Product]
    product = test_data_products[0]

    product_name_html = product_admin.product_name(product)
    assert isinstance(product_name_html, SafeString)
    assert "<a href=" in product_name_html
    assert product.name in product_name_html
