from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('account/orders/', views.orders_view, name='admin_orders'),
]