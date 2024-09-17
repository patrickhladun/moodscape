from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from apps.product.models import Product

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about', 'contact', 'privacy', 'terms', 'faq']
    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('product', args=[obj.slug])