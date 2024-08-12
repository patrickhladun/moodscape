from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import UpdateProductForm

from constance import config

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)

    template = "product/product.html"
    context = {
        "config" : config,
        "product": product,
    }
    return render(request, template, context)



@login_required
def products_view(request):
    user = request.user
    products = Product.objects.all()

    template = "product/admin/products.html"
    context = {
        'products': products,
        'config': config,
    }
    return render(request, template, context)


@login_required
def product_update_view(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProductForm(instance=product)

    template = "product/admin/product_update.html"
    context = {
        "product": product,
        "form": form
    }
    return render(request, template, context)