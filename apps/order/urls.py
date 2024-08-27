from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('account/orders/', views.orders_view, name='admin_orders'),
    path('account/orders/<order_number>/update/', 
        views.order_update_view, name='admin_order_update'),
]