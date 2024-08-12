import pytest

from unittest.mock import patch
from io import BytesIO
from PIL import Image

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.product.models import Product, Category

def test_category_meta_options():
    assert Category._meta.verbose_name == "Category"
    assert Category._meta.verbose_name_plural == "Categories"
    assert Category._meta.db_table == "mood_category"


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(
        name="Landscapes",
        slug="landscapes",
        description="Landscapes category"
    )
    assert category.name == "Landscapes"
    assert category.slug == "landscapes"
    assert str(category) == "Landscapes"


@pytest.mark.django_db
def test_category_slug_unique():
    Category.objects.create(
        name="Landscapes",
        slug="landscapes",
        description="Landscapes category"
    )

    with pytest.raises(ValidationError):
        duplicate_category = Category(
            name="Another Category",
            slug="landscapes",
            description="Another category description"
        )
        duplicate_category.full_clean()


def test_product_meta_options():
    assert Product._meta.verbose_name == "Product"
    assert Product._meta.verbose_name_plural == "Products"
    assert Product._meta.db_table == "mood_product"


@pytest.mark.django_db
def test_product_creation():
    category = Category.objects.create(
        name="Landscapes",
        slug="landscapes",
        description="Landscapes category"
    )
    product = Product.objects.create(
        name="Irish Coastal Sunset Watercolor",
        slug="irish-coastal-sunset-watercolor",
        details="A beautiful watercolor painting of an Irish coastal sunset.",
        sku="wat-orginal-1",
        stock=10,
        price=150.00,
        category=category,
        is_draft=False
    )
    assert product.name == "Irish Coastal Sunset Watercolor"
    assert product.slug == "irish-coastal-sunset-watercolor"
    assert product.sku == "wat-orginal-1"
    assert product.stock == 10
    assert product.price == 150.00
    assert product.category == category
    assert str(product) == "wat-orginal-1 - Irish Coastal Sunset Watercolor"


@pytest.mark.django_db
def test_product_fields():
    category = Category.objects.create(
        name="Landscapes",
        slug="landscapes",
        description="Landscapes category"
    )

    img_io = BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(img_io, format='WEBP')
    img_io.seek(0)

    image_file = SimpleUploadedFile(
        "irish-coastal-sunset-watercolor.webp",
        img_io.getvalue(),
        content_type="image/webp"
    )

    product = Product.objects.create(
        name="Irish Coastal Sunset Watercolor",
        slug="irish-coastal-sunset-watercolor",
        details="A beautiful watercolor painting of an Irish coastal sunset.",
        sku="wtc-ol-icsw1",
        stock=10,
        price=150.00,
        featured=image_file,
        is_draft=False,
        category=category
    )

    product.save()

    assert isinstance(product.name, str)
    assert isinstance(product.slug, str)
    assert isinstance(product.details, str)
    assert isinstance(product.sku, str)
    assert isinstance(product.stock, int)
    assert isinstance(product.featured, product._meta.get_field('featured').attr_class)
    assert isinstance(product.price, float)
    assert isinstance(product.is_draft, bool)

    with pytest.raises(ValidationError):
        product.name = "x" * 256
        product.full_clean()

    with pytest.raises(ValidationError):
        product.slug = "x" * 256
        product.full_clean()

    with pytest.raises(ValidationError):
        product.sku = "1" * 256
        product.full_clean()


@pytest.mark.django_db
def test_product_sku_unique():
    category = Category.objects.create(
        name="Landscapes",
        slug="landscapes",
        description="Landscapes category"
    )
    Product.objects.create(
        name="Irish Coastal Sunset Watercolor",
        slug="irish-coastal-sunset-watercolor",
        details="A beautiful watercolor painting of an Irish coastal sunset.",
        sku="1234567890",
        stock=10,
        price=150.00,
        featured="products/irish-coastal-sunset-watercolor.webp",
        category=category,
        is_draft=False
    )

    with pytest.raises(ValidationError):
        duplicate_product = Product(
            name="Another Product",
            slug="another-product",
            details="Another product description",
            sku="1234567890",
            stock=5,
            price=100.00,
            featured="products/irish-coastal-sunset-watercolor.webp",
            category=category,
            is_draft=False
        )
        duplicate_product.full_clean()

