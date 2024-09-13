from django.urls import path

from . import views

urlpatterns = [
    path("product/<str:slug>/", views.product_view, name="product"),
    path('cms/products/', views.cms_products_view, name='cms_products'),
    path("cms/products/add/", views.cms_product_add_view, name="cms_product_add"),
    path("cms/products/<int:id>/update/", views.cms_product_update_view, name="cms_product_update"),
    path("cms/products/<int:id>/delete/", views.cms_product_delete_view, name="cms_product_delete"),
    path("cms/categories/", views.cms_categories_view, name="cms_categories"),
    path("cms/categories/add/", views.cms_category_add_view, name="cms_category_add"),
    path("cms/categories/<int:id>/update/", views.cms_category_update_view, name="cms_category_update"),
    path("cms/categories/<int:id>/delete/", views.cms_category_delete_view, name="cms_category_delete"),
]