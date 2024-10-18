import os
import environ
from django.core.wsgi import get_wsgi_application

env = environ.Env()
env.read_env()

environment = env('ENVIRONMENT')

if environment == "production":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.production"
    )
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.development"
    )

application = get_wsgi_application()
