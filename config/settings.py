import os
import environ
from pathlib import Path
from collections import OrderedDict


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = []
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
EXTERNAL_APPS = [
    'allauth',
    'allauth.account',
    'constance',
    'constance.backends.database',
]
APPS = [
    'apps.common',
    'apps.frontend',
    'apps.product',
    'apps.user',
]
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "account"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
]
AUTH_USER_MODEL = "user.User"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/"
SITE_ID = 1
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env("GMAIL_EMAIL")
EMAIL_HOST_PASSWORD = env("GMAIL_PASS")
DEFAULT_FROM_EMAIL = env("GMAIL_EMAIL")
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = OrderedDict([
    ('SITE_NAME', ('Moodscape', 'The name of the site')),
    ('COPYRIGHT', ('All rights reserved.', 'Copyright information')),
    
    ('SHOP_ADDRESS', ('123 Main St', 'Shop address')),
    ('SHOP_MOBILE_PHONE', ('091456523', 'Shop mobile phone number')),
    ('SHOP_EMAIL', ('shop@moodscape.com', 'Shop email address')),
    
    ('CURRENCY', ('eur', 'Currency used in the shop')),
    ('CURRENCY_SYMBOL', ('€', 'Currency symbol')),
    ('FREE_DELIVERY_THRESHOLD', (50, 'Free delivery threshold amount')),
    ('STANDARD_DELIVERY_PERCENTAGE', (10, 'Standard delivery percentage')),
])
CONSTANCE_CONFIG_FIELDSETS = {
    'Site Settings': {
        'fields': ('SITE_NAME', 'COPYRIGHT'),},
    'Shop Details': {
        'fields': (
            'SHOP_ADDRESS', 
            'SHOP_MOBILE_PHONE', 
            'SHOP_EMAIL'
        ),
        'collapse': True
    },
    'Shop Settings': {
        'fields': (
            'CURRENCY',
            'CURRENCY_SYMBOL',
            'FREE_DELIVERY_THRESHOLD',
            'STANDARD_DELIVERY_PERCENTAGE',
        ),
        'collapse': True
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'