import factory
from factory import Faker
from factory.django import DjangoModelFactory
from apps.user.models import User

class SuperuserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = Faker("email")
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_staff = True
    is_superuser = True
    is_admin = True

