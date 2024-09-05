import factory
from factory import Faker
from factory.django import DjangoModelFactory
from apps.user.models import User, Customer
from apps.product.models import Product, Category
from apps.order.models import Order, OrderLineItem
from apps.review.models import Review

class SuperuserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = Faker("email")
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', '9aYezfQ+jVtlBLAHdQtW@Ojw')
    is_staff = True
    is_superuser = True
    is_admin = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True 

    email = Faker("email")
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'X$qza+pL&0LmPbssVLKKQT0l')
    is_admin = False
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def save_user(self, create, extracted, **kwargs):
        # Ensure the user is saved after setting the password
        if create:
            self.save()


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
        skip_postgeneration_save = True

    id = Faker("random_int")
    user = factory.SubFactory(UserFactory)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    phone_number = Faker("phone_number")
    country = Faker("country")
    postcode = Faker("postcode")
    town_city = Faker("city")
    address_line_1 = Faker("street_address")
    address_line_2 = Faker("secondary_address")
    county = Faker("state")
    image = ""
    created_at = Faker("date_time_this_year")
    updated_at = Faker("date_time_this_year")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    id = Faker("random_int")
    name = Faker("name")
    slug = Faker("slug")
    description = Faker("text")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("name")
    slug = Faker("slug")
    details = Faker("text")
    sku = Faker("ean13")
    stock = Faker("random_int", min=1, max=100)
    price = Faker("random_int", min=100, max=1000)
    is_published = False


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    order_number: Faker("random_int")
    email: Faker("email")
    first_name: Faker("first_name")
    last_name: Faker("last_name")
    phone_number: Faker("phone_number")
    country: Faker("country")
    postcode: Faker("postcode")
    town_city: Faker("city")
    address_line_1: Faker("street_address")
    address_line_2: Faker("secondary_address")
    county: Faker("state")
    shipping_cost: Faker("random_int", min=0, max=100)
    order_total: Faker("random_int", min=100, max=1000)
    grand_total: Faker("random_int", min=100, max=1000)
    status: Faker("random_element", elements=['processing', 'complete', 'cancelled'])
    created_at: Faker("date_time_this_year")
    updated_at: Faker("date_time_this_year")


class OrderLineItemFactory(DjangoModelFactory):
    
    class Meta:
        model = OrderLineItem
    
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = Faker("random_int", min=1, max=10)
    lineitem_total = Faker("random_int", min=100, max=1000)


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    id = Faker("random_int")
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    order_line_item = factory.SubFactory(OrderLineItemFactory)
    text = Faker("text")
    rating = Faker("random_int", min=1, max=5)
    created_at = Faker("date_time_this_year")
    updated_at = Faker("date_time_this_year")

