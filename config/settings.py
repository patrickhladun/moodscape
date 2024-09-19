import os
import environ
import dj_database_url
from pathlib import Path
from collections import OrderedDict

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))
env = environ.Env()

DEBUG = True
SECRET_KEY = env("SECRET_KEY")
ENVIRONMENT = os.getenv('ENVIRONMENT')
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]
EXTERNAL_APPS = [
    'allauth',
    'allauth.account',
    'constance',
    'constance.backends.database',
    'django_summernote',
    'compressor',
    'storages',
]
APPS = [
    'apps.bag',
    'apps.checkout',
    'apps.common',
    'apps.frontend',
    'apps.order',
    'apps.product',
    'apps.review',
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
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.frontend.context_processors.newsletter_form',
                'apps.bag.context.bag_contents',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
COMPRESS_ENABLED = True
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
    ('LOCALE', ('en_GB', 'Locale')),
    ('TWITTER', ('@moodscape', 'Twitter handle')),
    ('FACEBOOK', ('https://www.facebook.com/people/Moodscape/61566307404663/', 'Facebook page')),

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
        'fields': ('SITE_NAME', 'COPYRIGHT', 'LOCALE', 'TWITTER', 'FACEBOOK'),},
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
SUMMERNOTE_THEME = 'bs5'
SUMMERNOTE_CONFIG = {
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '280',
        'lang': None,
        'toolbar': [
            ['font', ['bold', 'underline', 'clear']],
            ['para', ['ul', 'ol']],
        ],
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')  

if ENVIRONMENT == 'development':
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    CSRF_TRUSTED_ORIGINS = ['http://localhost:3000',]
else:
    ALLOWED_HOSTS = ['moodscape-3f1dfd651cc4.herokuapp.com']
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = "codeinstitutefolder"
    AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_REGION_NAME = "eu-west-1"
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/moodscape/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/moodscape/media/"
    STATICFILES_LOCATION = 'moodscape/static'
    MEDIAFILES_LOCATION = 'moodscape/media'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }    
    DEFAULT_FILE_STORAGE = "config.utils.custom_storages.MediaStorage"
    STATICFILES_STORAGE = "config.utils.custom_storages.StaticStorage"

print(f"ENVIRONMENT: {ENVIRONMENT}")