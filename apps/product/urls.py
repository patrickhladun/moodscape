from django.urls import path

from . import views

urlpatterns = [
    path("product/<str:slug>/", 
        views.product_view, name="product"),
    path('account/products/', 
        views.products_view, name='admin_products'),
    path("account/products/add/", 
        views.product_add_view, name="admin_product_add"),
    path("account/products/<int:id>/update/", 
        views.product_update_view, name="admin_product_update"),
    path("account/products/<int:id>/delete/", 
        views.product_delete_view, name="admin_product_delete"),
    
    path("account/categories/", 
        views.categories_view, name="admin_categories"),
    path("account/categories/add/", 
        views.category_add_view, name="admin_category_add"),
    path("account/categories/<int:id>/update/", 
        views.category_update_view, name="admin_category_update"),
    path("account/categories/<int:id>/delete/", 
        views.category_delete_view, name="admin_category_delete"),
]