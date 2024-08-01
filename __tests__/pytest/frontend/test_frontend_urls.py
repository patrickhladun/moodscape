import pytest
from django.urls import URLPattern, URLResolver, reverse, resolve
from apps.frontend.urls import urlpatterns
from apps.frontend import views

def test_index_url_resolves():
    resolver = resolve('/')
    assert resolver.view_name == 'home'
    assert resolver.func == views.home
