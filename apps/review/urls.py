from django.urls import path
from . import views

urlpatterns = [
    path('cms/reviews/', views.cms_reviews_view, name='cms_reviews'),
    path('cms/reviews/<int:id>/update/', views.cms_review_update_view, name='cms_review_update'),
    path('account/reviews/', views.account_reviews_view, name='account_reviews'),
    path('account/reviews/<int:id>/submit/', views.account_review_submit_view, name='account_review_submit'),
    path('account/reviews/<int:id>/update/', views.account_review_update_view, name='account_resubmit_update_review'),
]