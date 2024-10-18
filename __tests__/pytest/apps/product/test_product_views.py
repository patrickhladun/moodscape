import pytest
from django.shortcuts import get_object_or_404
from django.test import Client
from django.urls import reverse

from __tests__.pytest.factories import (
    CategoryFactory,
    ProductFactory,
    SuperuserFactory,
)
from apps.frontend import views
from apps.product.models import Category, Product


@pytest.mark.django_db
def test_product_view(test_data_products):
    client = Client()

    product = test_data_products[0]
    response = client.get(reverse("product", args=[product.slug]))

    assert response.status_code == 200
    assert "product/product.html" in (t.name for t in response.templates)

    product = get_object_or_404(Product, slug=product.slug)

    assert (
        response.context["product"].name
        == "Original Watercolor Seascape Abstract Painting, Wall Art Abstract Art Purple."
    )
    assert (
        response.context["product"].slug
        == "irish-watercolor-seascape-abstract"
    )
    assert response.context["product"].sku == "wtc-ol-owsa1"
    assert response.context["product"].stock == 1
    assert response.context["product"].price == 168
    assert (
        response.context["product"].featured
        == "products/irish-watercolor-seascape-abstract.webp"
    )
    assert response.context["product"].category.name == "Watercolor"
    assert response.context["product"].is_published == False


@pytest.mark.django_db
def test_add_product_as_superadmin():
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("password")
    admin.save()

    client.force_login(admin)

    url = reverse("cms_product_add")
    category = CategoryFactory(id=2, name="Pen Plotter", slug="plotter")

    data = {
        "name": "Test Product",
        "slug": "",
        "details": "This is a test product.",
        "sku": "wtc-ol-tp1",
        "stock": 10,
        "price": 40.00,
        "category": category.id,
        "is_published": False,
    }

    response = client.post(url, data)

    assert (
        response.status_code == 302
    ), f"Form errors: {response.context['form'].errors}"

    try:
        product = Product.objects.get(name="Test Product")
    except Product.DoesNotExist:
        assert False, "Product was not created in the database."

    assert product.slug == "test-product"
    assert product.sku == "wtc-ol-tp1"
    assert product.stock == 10
    assert product.price == 40.00
    assert product.details == "This is a test product."
    assert product.is_published is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data,expected_error",
    [
        pytest.param(
            {
                "name": "",
                "slug": "",
                "details": "This is a test product with no name.",
                "sku": "wtc-ol-tp1",
                "stock": 10,
                "price": 40.00,
                "category": 1,
                "is_published": False,
            },
            "name",
            id="missing_name",
        ),
        pytest.param(
            {
                "name": "Test Product",
                "slug": "",
                "details": "This is a test product with a duplicate SKU.",
                "sku": "duplicate-sku",
                "stock": 10,
                "price": 40.00,
                "category": 1,
                "is_published": False,
            },
            "sku",
            id="duplicate_sku",
        ),
        pytest.param(
            {
                "name": "Test Product",
                "slug": "",
                "details": "This is a test product with a negative price.",
                "sku": "wtc-ol-tp2",
                "stock": 10,
                "price": "invalid-price",
                "category": 1,
                "is_published": False,
            },
            "price",
            id="invalid_price",
        ),
        pytest.param(
            {
                "name": "Test Product",
                "slug": "",
                "details": "This is a test product with a negative price.",
                "sku": "wtc-ol-tp2",
                "stock": 10,
                "price": -345.00,
                "category": 1,
                "is_published": False,
            },
            "price",
            id="negative_price",
        ),
        pytest.param(
            {
                "name": "Test Product",
                "slug": "",
                "details": "This is a test product with a negative price.",
                "sku": "wtc-ol-tp2",
                "stock": -10,
                "price": 40.00,
                "category": 1,
                "is_published": False,
            },
            "stock",
            id="negative_stock",
        ),
    ],
)
def test_add_product_with_invalid_data(data, expected_error):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("password")
    admin.save()

    client.force_login(admin)

    category = CategoryFactory(id=1, name="Pen Plotter", slug="plotter")
    data["category"] = category.id

    if expected_error == "sku":
        ProductFactory(sku="duplicate-sku", category=category)

    url = reverse("cms_product_add")

    response = client.post(url, data)

    assert response.status_code == 200
    assert (
        expected_error in response.context["form"].errors
    ), f"Expected error in {expected_error} field."


@pytest.mark.django_db
def test_category_view(test_data_categories):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("password")
    admin.save()

    client.force_login(admin)

    test_data_categories
    response = client.get(reverse("cms_categories"))

    assert response.status_code == 200
    assert "product/cms/categories.html" in (
        t.name for t in response.templates
    )
    assert len(response.context["categories"]) == 4


@pytest.mark.django_db
def test_add_category_as_superadmin():
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("password")
    admin.save()

    client.force_login(admin)

    url = reverse("cms_category_add")

    data = {
        "name": "Test Category",
        "slug": "test-category",
        "description": "This is a test category.",
    }

    response = client.post(url, data)

    assert (
        response.status_code == 302
    ), f"Form errors: {response.context['form'].errors}"

    try:
        category = Category.objects.get(name="Test Category")
    except Category.DoesNotExist:
        assert False, "Category was not created in the database."

    assert category.slug == "test-category"
    assert category.description == "This is a test category."


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data,expected_error",
    [
        pytest.param(
            {
                "name": "",
                "slug": "test-category",
                "description": "This is a test category with no name.",
            },
            "name",
            id="missing_name",
        ),
        pytest.param(
            {
                "name": "Test Category",
                "slug": "",
                "description": "This is a test category with no slug.",
            },
            "slug",
            id="missing_slug",
        ),
        pytest.param(
            {
                "name": "Test Category",
                "slug": "duplicated-slug",
                "description": "This is a test category with a duplicated slug.",
            },
            "slug",
            id="duplicated_slug",
        ),
    ],
)
def test_add_category_with_invalid_data(data, expected_error):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("password")
    admin.save()
    client.force_login(admin)

    if expected_error == "slug":
        CategoryFactory(slug="duplicated-slug")

    url = reverse("cms_category_add")
    response = client.post(url, data)

    assert response.status_code == 200
    assert expected_error in response.context["form"].errors
