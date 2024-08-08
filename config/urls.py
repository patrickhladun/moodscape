from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("apps.frontend.urls")),
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
]
