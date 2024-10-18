import pytest
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.review.models import Review
from apps.review.views import cms_reviews_view


@pytest.mark.django_db
def test_cms_reviews_view_unauthenticated(client):
    response = client.get(reverse("cms_reviews"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_cms_reviews_view_customer(client, test_customer):
    user = test_customer.user
    client.force_login(user)

    response = client.get(reverse("cms_reviews"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_cms_reviews_view_superuser(
    client, test_superuser, test_data_reviews
):
    client.force_login(test_superuser)

    test_data_reviews
    response = client.get(reverse("cms_reviews"))
    assert response.status_code == 200
    assert "review/cms/reviews.html" in (t.name for t in response.templates)
    assert len(response.context["reviews"]) == 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    "status, expected_count, validity",
    [
        ("pending", 3, True),
        ("pending", 4, False),
        ("approved", 3, True),
        ("approved", 4, False),
        ("rejected", 1, True),
        ("rejected", 2, False),
        ("deleted", 1, True),
        ("deleted", 4, False),
        ("", 3, True),
        ("invalid", 8, False),
    ],
)
def test_cms_reviews_view_filter_status(
    client,
    test_superuser,
    test_data_reviews,
    status,
    expected_count,
    validity,
):
    user = test_superuser
    client.force_login(user)

    test_data_reviews
    response = client.get(reverse("cms_reviews"), {"status": status})
    assert response.status_code == 200
    assert "review/cms/reviews.html" in (t.name for t in response.templates)
    if validity:
        assert len(response.context["reviews"]) == expected_count
    else:
        assert len(response.context["reviews"]) != expected_count


@pytest.mark.django_db
def test_cms_review_update_view_unauthenticated(client, test_data_reviews):
    test_review = test_data_reviews[0]
    url = reverse("cms_review_update", args=[test_review.id])
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_cms_review_update_view_customer(
    client, test_customer, test_data_reviews
):
    user = test_customer.user
    client.force_login(user)

    test_review = test_data_reviews[0]
    url = reverse("cms_review_update", args=[test_review.id])
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_cms_review_update_superuser(
    client, test_superuser, test_data_reviews
):
    client.force_login(test_superuser)

    review = test_data_reviews[3]
    assert review.status == "pending"

    url = reverse("cms_review_update", args=[review.id])

    update_data = {"update_status": True, "status": "approved"}

    response = client.post(url, update_data)

    assert response.status_code == 302

    review.refresh_from_db()

    assert review.status == "approved"

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Review status updated successfully."


@pytest.mark.django_db
def test_account_reviews_view_unauthenticated(client):
    response = client.get(reverse("account_reviews"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_account_reviews_view_authenticated_with_reviews(
    client, test_customers, test_data_reviews, test_data_order
):
    customer = test_customers[0]
    user = customer.user
    client.force_login(user)
    assert user.is_authenticated

    response = client.get(reverse("account_reviews"))
    assert (
        response.status_code == 200
    ), f"Response status code: {response.status_code}"
    assert "review/account/reviews.html" in [
        t.name for t in response.templates
    ]
    assert "reviews" in response.context

    user_reviews = Review.objects.filter(user=user)
    assert len(response.context["reviews"]) == 0

    pending_reviews = user_reviews.filter(status="pending")
    approved_reviews = user_reviews.filter(status="approved")
    rejected_reviews = user_reviews.filter(status="rejected")
    assert len(pending_reviews) == 0
    assert len(approved_reviews) == 1
    assert len(rejected_reviews) == 1


@pytest.mark.django_db
def test_account_review_submit_view_post(
    client, test_customer, test_data_order
):
    user = test_customer.user
    client.force_login(user)

    line_item = test_data_order.lineitems.first()
    product = line_item.product
    url = reverse("account_review_submit", args=[line_item.id])

    form_data = {
        "rating": 5,
        "text": "This is a great product!",
    }

    response = client.post(url, form_data)

    review = Review.objects.filter(
        user=user, product=product, order_line_item=line_item
    ).first()
    assert review is not None
    assert review.rating == 5
    assert review.text == "This is a great product!"
    assert review.user == user
    assert review.product == product
    assert review.order_line_item == line_item

    messages_list = list(response.wsgi_request._messages)
    assert len(messages_list) == 1
    assert str(messages_list[0]) == "Review submitted successfully."
