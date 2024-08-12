import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory

@pytest.mark.django_db
def test_admin_navigation_active_account():
    request = RequestFactory().get('/account/')
    rendered_template = render_to_string('partials/nav_admin.html', {'request': request})
    
    assert 'class="admin-nav-item active"' in rendered_template
    assert 'href="/account/"' in rendered_template

    assert 'href="/account/products/"' in rendered_template
    assert 'class="admin-nav-item"' in rendered_template.split('href="/account/products/"')[1]

@pytest.mark.django_db
def test_admin_navigation_active_products():
    request = RequestFactory().get('/account/products/')
    
    rendered_template = render_to_string('partials/nav_admin.html', {'request': request})
    
    assert 'class="admin-nav-item active"' in rendered_template
    assert 'href="/account/products/"' in rendered_template

    assert 'href="/account/"' in rendered_template
    assert 'class="admin-nav-item"' in rendered_template.split('href="/account/"')[1]
