from django.urls import path

from . import views
from .webhooks import webhook_stripe

urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path(
        "checkout_success/<order_number>",
        views.checkout_success_view,
        name="checkout_success",
    ),
    path(
        "checkout/cache_checkout_data/",
        views.cache_checkout_data,
        name="cache_checkout_data",
    ),
    path("webhooks/stripe/", webhook_stripe, name="webhook_stripe"),
]
