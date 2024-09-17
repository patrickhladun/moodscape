from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("apps.bag.urls")),
    path("", include("apps.common.urls")),
    path("", include("apps.checkout.urls")),
    path("", include("apps.frontend.urls")),
    path("", include("apps.order.urls")),
    path("", include("apps.product.urls")),
    path("", include("apps.review.urls")),
    path("", include("apps.user.urls")),
]

urlpatterns += [path('admin/', admin.site.urls)]
urlpatterns += [path('account/', include('allauth.urls'))]
urlpatterns += [path('summernote/', include('django_summernote.urls'))]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)