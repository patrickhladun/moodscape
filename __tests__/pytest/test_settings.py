import os
import pytest
from django.conf import settings

def test_environment_variables():
    assert settings.EMAIL_HOST_USER is not None
    assert settings.EMAIL_HOST_PASSWORD is not None


def test_static_url():
    assert settings.STATIC_URL == '/static/'


def test_media_url():
    assert settings.MEDIA_URL == '/media/'
    assert os.path.exists(settings.MEDIA_ROOT)


def test_email_settings():
    assert settings.EMAIL_HOST == "smtp.gmail.com"
    assert settings.EMAIL_PORT == 587
    assert settings.EMAIL_USE_TLS is True
    assert settings.EMAIL_USE_SSL is False
    assert settings.EMAIL_HOST_USER is not None
    assert settings.EMAIL_HOST_PASSWORD is not None


def test_constance_settings():
    assert settings.CONSTANCE_CONFIG['SITE_NAME'][0] == 'Moodscape'
    assert settings.CONSTANCE_CONFIG['COPYRIGHT'][0] == 'All rights reserved.'
    assert settings.CONSTANCE_CONFIG['SHOP_ADDRESS'][0] == '123 Main St'
    assert settings.CONSTANCE_CONFIG['SHOP_MOBILE_PHONE'][0] == '091456523'
    assert settings.CONSTANCE_CONFIG['SHOP_EMAIL'][0] == 'shop@moodscape.com'
    assert settings.CONSTANCE_CONFIG['CURRENCY'][0] == 'eur'
    assert settings.CONSTANCE_CONFIG['CURRENCY_SYMBOL'][0] == '€'
    assert settings.CONSTANCE_CONFIG['FREE_DELIVERY_THRESHOLD'][0] == 50
    assert settings.CONSTANCE_CONFIG['STANDARD_DELIVERY_PERCENTAGE'][0] == 10
