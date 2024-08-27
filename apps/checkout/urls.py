from django.urls import path
from . import views
from .views import checkout_view, checkout_success_view

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success_view, name='checkout_success'),
]