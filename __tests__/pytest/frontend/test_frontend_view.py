import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 200
    assert 'frontend/index.html' in [t.name for t in response.templates]
