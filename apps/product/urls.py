from django.urls import path

from . import views

urlpatterns = [
    path("product/<str:slug>/", views.product_view, name="product"),

    path('account/products/', views.products_view, name='admin_products'),
    path("account/products/<int:id>/", views.product_update_view, name="product_update"),
]