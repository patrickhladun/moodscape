from django.urls import path
from . import views

urlpatterns = [
    path('cms/customers/', views.cms_customers_view, name='cms_customers'),
    path('account/', views.account_view, name='account'),
    path('account/profile/', views.account_profile_view, name='account_profile'),
]