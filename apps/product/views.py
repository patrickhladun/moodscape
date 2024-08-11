from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Product
from constance import config

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)

    template = "product/product.html"
    context = {
        "config" : config,
        "product": product,
    }
    return render(request, template, context)