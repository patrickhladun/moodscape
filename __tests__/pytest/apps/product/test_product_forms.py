import pytest

from apps.product.forms import ProductForm, CategoryForm
from __tests__.pytest.factories import CategoryFactory

@pytest.mark.django_db
def test_product_form_initial_state():
    form = ProductForm()
    assert not form.is_bound
  

@pytest.mark.django_db
def test_product_form_with_valid_data():

    category = CategoryFactory()

    form_data = {
        "name": "Product 1",
        "slug": "product-1",
        "details": "This is a test product.",
        "sku": "SKU123",
        "stock": 10,
        "price": 100.00,
        "category": category.id,
        "is_published": True,
    }
    form = ProductForm(data=form_data)
    assert form.is_bound
    assert form.is_valid(), form.errors
    assert form.cleaned_data["name"] == "Product 1"
    assert form.cleaned_data["slug"] == "product-1"
    assert form.cleaned_data["details"] == "This is a test product."
    assert form.cleaned_data["sku"] == "SKU123"
    assert form.cleaned_data["stock"] == 10
    assert form.cleaned_data["price"] == 100.00
    assert form.cleaned_data["category"] == category
    assert form.cleaned_data["is_published"] == True


@pytest.mark.django_db
def test_product_form_with_empty_data():
    form_data = {}
    form = ProductForm(data=form_data)
    assert form.is_bound
    assert not form.is_valid()
    assert "name" in form.errors
    assert "sku" in form.errors
    assert "stock" in form.errors
    assert "price" in form.errors
    assert "category" in form.errors
    assert form.errors["name"] == ["This field is required."]
    assert form.errors["sku"] == ["This field is required."]
    assert form.errors["stock"] == ["This field is required."]
    assert form.errors["price"] == ["This field is required."]
    assert form.errors["category"] == ["This field is required."]


@pytest.mark.django_db
@pytest.mark.parametrize("name,expected_slug", [
    pytest.param(
      "Product 1", "product-1", id="generate_slug_simple"
    ),
    pytest.param(
        "Test Product ...", "test-product", id="generate_slug_with_dots"
    ),
    pytest.param(
        "Test: Product", "test-product", id="generate_slug_with_colon"
    ),
    pytest.param(
        "New Product!", "new-product", id="generate_slug_with_exclamation"
    ),
    pytest.param(
        "Product@2024", "product2024", id="generate_slug_with_at_symbol"
    ),
    pytest.param(
        "   Product 1   ", "product-1", id="generate_slug_with_extra_spaces"
    ),
    pytest.param(
        "Product#1", "product1", id="generate_slug_with_hash"
    ),
    pytest.param(
        "Amazing Product?", "amazing-product", id="generate_slug_with_question_mark"
    ),
    pytest.param(
        "Cool & Trendy Product", "cool-trendy-product", id="generate_slug_with_ampersand"
    ),
    pytest.param(
        "Test Product - Limited Edition", "test-product-limited-edition", id="generate_slug_with_dash"
    ),
    pytest.param(
        "Test Product + Special", "test-product-special", id="generate_slug_with_plus"
    ),
    pytest.param(
        "50% Off Product", "50-off-product", id="generate_slug_with_percent_sign"
    ),
    pytest.param(
        "Product (Special Edition)", "product-special-edition", id="generate_slug_with_parentheses"
    ),
    pytest.param(
        "Product_2024", "product_2024", id="generate_slug_with_underscore"
    ),
    pytest.param(
        "Product 2024-", "product-2024", id="generate_slug_without_ending_dash"
    ),
])
def test_product_form_slug_generation(name, expected_slug):
    category = CategoryFactory()
    form_data = {
        "name": name,
        "slug": "",
        "details": "This is a test product.",
        "sku": "SKU123",
        "stock": 10,
        "price": 100.00,
        "category": category.id,
        "is_published": True,
    }
    form = ProductForm(data=form_data)
  
    assert form.is_valid(), form.errors
    assert form.cleaned_data["slug"] == expected_slug


@pytest.mark.django_db
def test_product_stock_validation():
    """
      Test the stock validation in the ProductForm.

      This test ensures that the ProductForm correctly identifies and handles
      cases where the 'stock' value is negative. The form should be invalid 
      if the stock is negative, and an appropriate error message should be 
      returned.
    """
    category = CategoryFactory()
    form_data = {
        "name": "Product 1",
        "slug": "product-1",
        "details": "This is a test product.",
        "sku": "SKU123",
        "stock": -10,
        "price": 100.00,
        "category": category.id,
        "is_published": True,
    }
    form = ProductForm(data=form_data)
    assert not form.is_valid()
    assert form.errors["stock"] == ["Stock cannot be negative."]



@pytest.mark.django_db
def test_product_form_details_field_type():
    form = ProductForm()
    assert form.fields["details"].widget.__class__.__name__ == "SummernoteWidget"
