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
    path("cms/faqs/", views.cms_faqs_view, name="cms_faqs"),
    path("cms/faqs/add/", views.cms_faqs_add_view, name="cms_faqs_add"),
    path(
        "cms/faqs/<int:id>/update/",
        views.cms_faqs_update_view,
        name="cms_faqs_update",
    ),
    path(
        "cms/faqs/<int:id>/delete/",
        views.cms_faqs_delete_view,
        name="cms_faqs_delete",
    ),
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
