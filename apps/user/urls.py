from django.urls import path
from . import views

urlpatterns = [
    path('cms/customers/', views.cms_customers_view, name='cms_customers'),
    path('cms/customers/<int:id>/update/', views.cms_customer_update_view, name='cms_customer_update'),
    path("cms/customers/<int:id>/delete/", views.cms_customer_delete_view, name="cms_customer_delete"),
    path('account/', views.account_view, name='account'),
    path('account/profile/', views.account_profile_view, name='account_profile'),
]