import pytest
from pytest_factoryboy import register

from .factories import ProductFactory, CategoryFactory


@pytest.fixture
def test_data_categories():
  category_1 = CategoryFactory(
    name="Watercolor",
    slug="watercolor",
    description="Watercolor paints"
  ) 
  category_2 = CategoryFactory(
    name="Photography",
    slug="photography",
    description="Photography prints"
  )
  
  return [category_1, category_2]


@pytest.fixture
def test_data_products():
  category_1 = CategoryFactory(
    name="Watercolor",
    slug="watercolor",
    description="Watercolor paints"
  ) 
  category_2 = CategoryFactory(
    name="Photography",
    slug="photography",
    description="Photography prints"
  )

  product_1 = ProductFactory(
    name="Irish Coastal Sunset Watercolor",
    slug="irish-coastal-sunset-watercolor",
    details="",
    sku="wtc-ol-icsw1",
    stock=10,
    price=128,
    featured="products/irish-coastal-sunset-watercolor.webp",
    category=category_1,
    is_draft=False
  )

  product_2 = ProductFactory(
    name="Abstract Irish Cliffs Oil Painting",
    slug="abstract-irish-cliffs-oil-painting",
    details="",
    sku="wtc-pt-aico1",
    stock=3,
    price=42,
    featured="products/abstract-irish-cliffs-oil-painting.webp",
    category=category_1,
    is_draft=False
  )

  product_3 = ProductFactory(
    name="Tranquil Irish Ocean Waves Print",
    slug="tranquil-irish-ocean-waves-print",
    details="",
    sku="wtc-pt-tiow1",
    stock=4,
    price=120,
    featured="products/tranquil-irish-ocean-waves-print.webp",
    category=category_1,
    is_draft=False
  )

  product_4 = ProductFactory(
    name="Golden Marguerite Close-Up Photograph",
    slug="golden-marguerite-close-up-photograph",
    details="",
    sku="wtc-po-gmcu1",
    stock=4,
    price=52,
    featured="products/golden-marguerite-close-up-photograph.webp",
    category=category_2,
    is_draft=False
  )

  product_5 = ProductFactory(
    name="Vibrant Red Poppy Petals Macro Shot",
    slug="vibrant-red-poppy-petals-macro-shot",
    details="",
    sku="wtc-po-vrpp1",
    stock=8,
    price=52,
    featured="products/vibrant-red-poppy-petals-macro-shot.webp",
    category=category_2,
    is_draft=False
  ) 

  product_6 = ProductFactory(
    name="White Marguerite Blossom Macro Print",
    slug="white-marguerite-blossom-macro-print",
    details="",
    sku="wtc-po-wmbm1",
    stock=3,
    price=52,
    featured="products/white-marguerite-blossom-macro-print.webp",
    category=category_2,
    is_draft=False
  )
  
  return [product_1, product_2, product_3, product_4, product_5, product_6]
