from django.urls import path

from . import views

urlpatterns = [
    path("cms/orders/", views.cms_orders_view, name="cms_orders"),
    path(
        "cms/orders/<order_number>/update/",
        views.cms_order_update_view,
        name="cms_order_update",
    ),
    path(
        "account/orders/", views.account_orders_view, name="account_orders"
    ),
    path(
        "account/orders/<order_number>/",
        views.account_order_view,
        name="account_order",
    ),
]
