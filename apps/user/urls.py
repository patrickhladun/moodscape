from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account_view, name='admin_account'),
    path('account/', views.account_view, name='account'),
    path('account/profile/', views.account_profile_view, name='account_profile'),
]