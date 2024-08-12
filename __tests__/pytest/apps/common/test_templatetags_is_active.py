import pytest

from django.template import Context
from django.http import HttpRequest

from apps.common.templatetags.ui_tags import active

@pytest.mark.django_db
def test_active_exact_match():
    request = HttpRequest()
    request.path = '/account/'

    context = Context({'request': request, 'active': 'account'})

    result = active(context, 'account')
    assert result == ' active'

    result = active(context, 'products')
    assert result == ''