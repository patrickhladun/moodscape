from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("faq/", views.faq, name="faq"),
    path("shop/", views.shop, name="shop"),
]
