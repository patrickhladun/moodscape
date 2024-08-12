from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account_view, name='admin_account'),
]