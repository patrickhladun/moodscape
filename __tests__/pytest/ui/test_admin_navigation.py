import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory

@pytest.mark.django_db
def test_cms_navigation_active_account():
    request = RequestFactory().get('/account/')
    rendered_template = render_to_string('partials/nav_account.html', {'request': request, 'active': 'account'})
    
    assert 'class="admin-nav-item active"' in rendered_template
    assert 'href="/account/"' in rendered_template


@pytest.mark.django_db
def test_cms_navigation_active_products():
    request = RequestFactory().get('/cms/products/')
    rendered_template = render_to_string('partials/nav_cms.html', {'request': request, 'active': 'products'})
    
    assert 'class="admin-nav-item active"' in rendered_template
    assert 'href="/cms/products/"' in rendered_template
