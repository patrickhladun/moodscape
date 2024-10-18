import pytest
from django.test import Client
from django.urls import URLPattern, URLResolver, resolve, reverse

from apps.bag import views
from apps.bag.urls import urlpatterns


@pytest.mark.django_db
def test_no_empty_path():
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            assert pattern.pattern._route != "", "Empty path pattern found!"
        elif isinstance(pattern, URLResolver):
            # Recursively check included URL configurations
            for sub_pattern in pattern.url_patterns:
                assert (
                    sub_pattern.pattern._route != ""
                ), "Empty path pattern found in included urls!"
