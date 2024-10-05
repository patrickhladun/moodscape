from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.success_contact, name="success_contact"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("faq/", views.faq, name="faq"),
    path("shop/", views.shop, name="shop"),
]

urlpatterns += [
    path(
        "newsletter/subscribe/",
        views.newsletter_subscribe,
        name="newsletter_subscribe",
    ),
    path(
        "newsletter/success/",
        views.success_newsletter,
        name="success_newsletter",
    ),
]
