import pytest

from django.urls import URLPattern, URLResolver, reverse, resolve
from django.test import Client

from apps.review.urls import urlpatterns
from apps.review import views


@pytest.mark.django_db
def test_no_empty_path():
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            assert pattern.pattern._route != "", "Empty path pattern found!"
        elif isinstance(pattern, URLResolver):
            # Recursively check included URL configurations
            for sub_pattern in pattern.url_patterns:
                assert sub_pattern.pattern._route != "", "Empty path pattern found in included urls!"



@pytest.mark.django_db
def test_cms_reviews_url():
    url = reverse('cms_reviews')
    assert resolve(url).func == views.cms_reviews_view

@pytest.mark.django_db
def test_cms_review_update_url():
    url = reverse('cms_review_update', args=[1])
    assert resolve(url).func == views.cms_review_update_view

@pytest.mark.django_db
def test_account_reviews_url():
    url = reverse('account_reviews')
    assert resolve(url).func == views.account_reviews_view

@pytest.mark.django_db
def test_account_review_submit_url():
    url = reverse('account_review_submit', args=[1])
    assert resolve(url).func == views.account_review_submit_view
