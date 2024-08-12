import pytest

from django.http import HttpRequest

from apps.common.templatetags.ui_tags import is_active

@pytest.mark.django_db
def test_is_active_exact_match():
    request = HttpRequest()
    request.path = '/account/'

    result = is_active(request, '/account/')
    assert result == ' active'

    result = is_active(request, '/account/products/')
    assert result == ''


