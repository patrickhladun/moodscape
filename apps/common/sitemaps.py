from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from apps.product.models import Product


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static views like 'about', 'contact', 'privacy', 'terms',
    and 'faq'.

    The sitemap generates URLs for static pages using Django's reverse
    function.
    """

    def items(self):
        return ["about", "contact", "privacy", "terms", "faq"]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    """
    Sitemap for product pages.

    The sitemap generates URLs for all products, with a weekly change frequency
    and a high priority. The 'lastmod' attribute reflects the last time each
    product was updated.
    """

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("product", args=[obj.slug])
