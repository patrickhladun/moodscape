from django.urls import path

from . import views

urlpatterns = [
    path("product/<str:slug>/", views.product_view, name="product"),
]