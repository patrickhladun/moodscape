import pytest

from django.test import Client
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.frontend import views
from apps.order.models import Order, OrderLineItem

from __tests__.pytest.factories import SuperuserFactory, OrderFactory, OrderLineItemFactory


@pytest.mark.django_db
def test_cms_order_update_view_update_status(test_data_orders):
    """
    Test that the order status is updated successfully when 'update_status' is posted.
    """
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("cjTvdv#V9tRyr+X179bW@lol")
    admin.save()

    client.force_login(admin)

    order = test_data_orders[0]

    form_data = {
        'update_status': 'true',
        'status': 'complete'
    }

    url = reverse('cms_order_update', args=[order.order_number])
    response = client.post(url, data=form_data)

    order.refresh_from_db()
    assert response.status_code == 302
    assert order.status == 'complete'
    assert 'Order status updated successfully.' in [msg.message for msg in response.wsgi_request._messages] 


@pytest.mark.django_db
def test_cms_order_update_view_update_form(test_data_orders):
    """
    Test that the order is updated successfully when 'update_form' is posted.
    """
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("55W5DDUObqxwag8l6XiNjF$a")
    admin.save()

    client.force_login(admin)

    order = test_data_orders[0]

    form_data = {
        'update_form': 'true',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone_number': '1234567890',
        'country': 'US',
        'postcode': '12345',
        'town_city': 'New York',
        'address_line_1': '123 Main St',
        'address_line_2': 'Apt 1',
        'county': 'New York',
    }

    url = reverse('cms_order_update', args=[order.order_number])
    response = client.post(url, data=form_data)

    order.refresh_from_db()
    assert response.status_code == 302
    assert 'Order updated successfully.' in [msg.message for msg in response.wsgi_request._messages]
    assert order.first_name == 'John'
    assert order.last_name == 'Doe'
    assert order.email == 'johndoe@example.com'
    assert order.phone_number == '1234567890'
    assert order.country == 'US'
    assert order.postcode == '12345'
    assert order.town_city == 'New York'
    assert order.address_line_1 == '123 Main St'
    assert order.address_line_2 == 'Apt 1'
    assert order.county == 'New York'


@pytest.mark.django_db
def test_cms_order_update_view_add_item(test_data_order, test_data_line_items):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("znrk4#cUAMdN!0eA4eYB9sxa")
    admin.save()

    client.force_login(admin)

    order = test_data_order
    line_item = test_data_line_items[2]

    form_data = {
        'add_item': 'true',
        'product': line_item.product.id,
        'quantity': 2,
    }

    url = reverse('cms_order_update', args=[order.order_number])
    response = client.post(url, data=form_data)

    order.refresh_from_db()

    assert response.status_code == 302
    assert order.lineitems.count() == 4
    assert 'Item added successfully.' in [msg.message for msg in response.wsgi_request._messages]


@pytest.mark.django_db
def test_cms_order_update_view_update_item(test_data_order, test_data_products):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("1S65lea9#9AAlM0JMzqprSbT")
    admin.save()
    client.force_login(admin)

    order = test_data_order
    item_to_update = order.lineitems.first()
    product = test_data_products[6]

    form_data = {
        'update_item': 'true',
        'item_id': item_to_update.id,
        'product': product.id,
        'quantity': 2,
    }

    url = reverse('cms_order_update', args=[order.order_number])
    response = client.post(url, data=form_data)

    order.refresh_from_db()

    assert response.status_code == 302
    assert order.lineitems.count() == 3
    updated_item = order.lineitems.get(id=item_to_update.id)
    assert updated_item.product == product
    assert updated_item.quantity == 2
    assert 'Item updated successfully.' in [msg.message for msg in response.wsgi_request._messages]


@pytest.mark.django_db
def test_cms_order_update_view_delete_item(test_data_order, test_data_line_items):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("1z4EvuUOkOdzF##vUudCe6O9")
    admin.save()
    client.force_login(admin)

    order = test_data_order

    form_data = {
        'delete_item': 'true',
        'item_id': order.lineitems.first().id,
    }

    url = reverse('cms_order_update', args=[order.order_number])
    response = client.post(url, data=form_data)

    order.refresh_from_db()

    assert response.status_code == 302
    assert order.lineitems.count() == 2


@pytest.mark.django_db
def test_cms_orders_view(test_data_orders):
    client = Client()

    admin = SuperuserFactory()
    admin.set_password("&2H+WzXzkTSr+ntUSxzXggfa")
    admin.save()

    client.force_login(admin)

    test_data_orders

    url = reverse('cms_orders')
    response = client.get(url)

    assert response.status_code == 200
    assert "order/cms/orders.html" in (t.name for t in response.templates)

    orders = response.context["orders"]
    assert len(orders) == 3
    assert orders[2].customer is not None
