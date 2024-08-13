from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category
from .forms import AddProductForm, UpdateProductForm, CategoryForm

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
        'active': 'products'
    }
    return render(request, template, context)


@login_required
def product_add_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect(reverse('admin_product_update', args=[form.instance.id]))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AddProductForm()

    template = "product/admin/product_add.html"
    context = {
        "form": form,
        'active': 'products'
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
        "form": form,
        'active': 'products'
    }
    return render(request, template, context)


@login_required
def product_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect(reverse('admin_products'))
    
    template = "product/admin/products.html"
    context = {
        "product": product,
        'active': 'products'
    }
    return render(request, template, context)


@login_required
def categories_view(request):
    user = request.user
    categories = Category.objects.all()

    template = "product/admin/categories.html"
    context = {
        'categories': categories,
        'active': 'categories'
    }

    return render(request, template, context)


def category_update_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CategoryForm(instance=category)

    template = "product/admin/category_update.html"
    context = {
        "category": category,
        "form": form,
        'active': 'categories'
    }
    return render(request, template, context)


def category_delete_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect(reverse('admin_categories'))
    
    template = "product/admin/categories.html"
    context = {
        "category": category,
        'active': 'categories'
    }
    return render(request, template, context)


def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect(reverse('admin_categories'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CategoryForm()

    template = "product/admin/category_add.html"
    context = {
        "form": form,
        'active': 'categories'
    }
    return render(request, template, context)