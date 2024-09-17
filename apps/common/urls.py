from django.urls import path
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticViewSitemap, ProductSitemap

from .views import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps})
]