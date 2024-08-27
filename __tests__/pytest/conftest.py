import pytest
from pytest_factoryboy import register

from .factories import (
  ProductFactory, CategoryFactory, UserFactory, 
  CustomerFactory, OrderFactory, OrderLineItemFactory
)


register(ProductFactory)
register(CategoryFactory)
register(UserFactory)
register(CustomerFactory)
register(OrderFactory)
register(OrderLineItemFactory)


@pytest.fixture
def test_data_categories():
    category_1 = CategoryFactory(
        id=1,
        name="Undefined",
        slug="undefined",
        description="Undefined category"
    )
    category_2 = CategoryFactory(
        id=2,
        name="Watercolor",
        slug="watercolor",
        description="Watercolor paints"
    ) 
    category_3 = CategoryFactory(
        id=3,
        name="Photography",
        slug="photography",
        description="Photography prints"
    )
    category_4 = CategoryFactory(
        id=4,
        name="Digital Art",
        slug="digital-art",
        description="Digital art prints"
    )
    
    return [category_1, category_2, category_3, category_4]


@pytest.fixture
def test_data_products(test_data_categories):
    category_1, category_2, category_3 = test_data_categories[1], test_data_categories[2], test_data_categories[3]

    product_1 = ProductFactory(
        id=1,
        name="Original Watercolor Seascape Abstract Painting, Wall Art Abstract Art Purple.",
        slug="irish-watercolor-seascape-abstract",
        details="",
        sku="wtc-ol-owsa1",
        stock=1,
        price=168,
        featured="products/irish-watercolor-seascape-abstract.webp",
        category=category_1,
        is_published=False
    )

    product_2 = ProductFactory(
        id=2,
        name="Watercolor Abstract Art Indigo",
        slug="abstract-watercolor-indigo",
        details="",
        sku="wtc-pt-awsd1",
        stock=1,
        price=168,
        featured="products/abstract-watercolor-indigo.webp",
        category=category_1,
        is_published=False
    )

    product_3 = ProductFactory(
        id=3,
        name="Abstract Irish Landscape Watercolor Original Painting Abstract Art Galway",
        slug="abstract-irish-landscape-watercolor",
        details="",
        sku="wtc-pt-awsd2",
        stock=1,
        price=168,
        featured="products/abstract-irish-landscape-watercolor.webp",
        category=category_1,
        is_published=False
    )

    product_4 = ProductFactory(
        id=4,
        name="Macro Shot of Small Flowers with Stunning White, Yellow, and Purple Colors",
        slug="small-flowers-stunning-colors",
        details="<p>This breathtaking macro shot captures the delicate beauty of small flowers, showcasing their stunning colors of white, yellow, and purple. The intricate details and vibrant hues create a captivating visual experience.</p><p>The photograph is printed on high-resolution Giclée Art Paper Hahnemühle Photo RAG 308, ensuring that the vivid colors and fine details are rendered with exceptional clarity.</p><p><strong>Size:</strong> 297x297mm</p><p>Please note that tones and colors may differ slightly depending on the monitor or screen used for viewing the artwork.</p><p>Your order will be shipped with a tracking number to ensure it reaches you safely.</p>",
        sku="photo-msos",
        stock=4,
        price=120,
        featured="products/small-flowers-stunning-colors.webp",
        category=category_2,
        is_published=False
    )

    product_5 = ProductFactory(
        id=5,
        name="Macro Shot of Dandelion with Seeds Scattered",
        slug="dandelion-missing-seeds",
        details="<p>This striking macro shot captures a dandelion with many of its seeds already blown away, revealing the intricate structure and delicate beauty of what remains. The fine details and natural textures make this image both captivating and evocative.</p><p>The photograph is printed on high-resolution Giclée Art Paper Hahnemühle Photo RAG 308, ensuring that the subtle nuances and fine details are rendered with stunning clarity.</p><p><strong>Size:</strong> 297x297mm</p><p>Please note that tones and colors may differ slightly depending on the monitor or screen used for viewing the artwork.</p><p>Your order will be shipped with a tracking number to ensure it reaches you safely.</p>",
        sku="photo-ddms",
        stock=8,
        price=88,
        featured="products/dandelion-missing-seeds.webp",
        category=category_2,
        is_published=False
    ) 

    product_6 = ProductFactory(
        id=6,
        name="Withered Daisy After Bloom",
        slug="withered-daisy-bloom",
        details="<p>This evocative photograph captures a large Daisy flower after the season has passed, standing bare without its leaves. The image highlights the raw beauty of nature in its cycle, with intricate details and textures that tell a story of resilience and change.</p><p>The photograph is printed on high-resolution Giclée Art Paper Hahnemühle Photo RAG 308, ensuring that the fine details and natural tones are rendered with stunning clarity.</p><p><strong>Size:</strong> 297x297mm</p><p>Please note that tones and colors may differ slightly depending on the monitor or screen used for viewing the artwork.</p><p>Your order will be shipped with a tracking number to ensure it reaches you safely.</p>",
        sku="photo-wdab",
        stock=3,
        price=88,
        featured="products/withered-daisy-bloom.webp",
        category=category_2,
        is_published=False
    )

    product_7 = ProductFactory(
        id=7,
        name="Blue Waves, Gold Triangles on Black Background Pen Plotter Abstract Art",
        slug="blue-waves-gold-black",
        details="<p>This stunning pen plotter abstract art features flowing blue waves contrasted with sharp gold triangles, all set against a deep black background. The artwork is printed on Giclée Art Paper Hahnemühle German Etching 310, highlighting the intricate design with rich textures and depth.</p><p><strong>Size:</strong> 297x297mm</p><p>Please note that tones and colors may differ slightly depending on the monitor or screen used for viewing the artwork.</p><p>Your order will be shipped with a tracking number to ensure it reaches you safely.</p>",
        sku="ppl-pl-bwgb1",
        stock=3,
        price=148.00,
        featured="products/blue-waves-gold-black.webp",
        category=category_3,
        is_published=False
    )

    product_8 = ProductFactory(
        id=8,
        name="Mathematical Abstract Plotted with Green Gradient on Black",
        slug="mathematical-abstract-plotted",
        details="<p>This captivating pen plotter art showcases a mathematical abstract design, plotted with a striking green gradient on a deep black background. The complex patterns and gradient effect create a visually stunning piece. The artwork is printed on Giclée Art Paper Hahnemühle German Etching 310, bringing out the intricate details with rich textures.</p><p><strong>Size:</strong> 297x297mm</p><p>Please note that tones and colors may differ slightly depending on the monitor or screen used for viewing the artwork.</p><p>Your order will be shipped with a tracking number to ensure it reaches you safely.</p>",
        sku="ppl-pl-mapg1",
        stock=3,
        price=148.00,
        featured="products/mathematical-abstract-plotted.webp",
        category=category_3,
        is_published=False
    )
    
    return [product_1, product_2, product_3, product_4, product_5, product_6, product_7, product_8]


@pytest.fixture
def test_data_line_items(test_data_products):
    line_item_1 = OrderLineItemFactory(product=test_data_products[1], quantity=1)
    line_item_2 = OrderLineItemFactory(product=test_data_products[2], quantity=2)
    line_item_3 = OrderLineItemFactory(product=test_data_products[3], quantity=2)

    return [line_item_1, line_item_2, line_item_3]


@pytest.fixture
def test_data_order(test_data_products):
    customer = CustomerFactory()
    order = OrderFactory(customer=customer)
    line_item_1 = OrderLineItemFactory(order=order, product=test_data_products[0], quantity=1)
    line_item_2 = OrderLineItemFactory(order=order, product=test_data_products[3], quantity=1)
    line_item_3 = OrderLineItemFactory(order=order, product=test_data_products[7], quantity=2)

    return order


@pytest.fixture
def test_data_orders():
    customer_1 = CustomerFactory()
    customer_2 = CustomerFactory()

    order_1 = OrderFactory(customer=customer_1)
    order_2 = OrderFactory(customer=customer_2)
    order_3 = OrderFactory()

    return [order_1, order_2, order_3]