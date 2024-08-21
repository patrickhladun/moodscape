from django.urls import path
from . import views


urlpatterns = [
    path('bag/', views.bag_view, name='bag'),
    path('add_to_bag/<id>/', views.add_to_bag_view, name='add_to_bag'),
]