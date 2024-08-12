import factory
from factory import Faker
from factory.django import DjangoModelFactory
from apps.user.models import User
from apps.product.models import Product, Category

class SuperuserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = Faker("email")
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = True
    is_superuser = True
    is_admin = True



class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

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
