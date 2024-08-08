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
