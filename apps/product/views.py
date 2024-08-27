from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from constance import config
from apps.common.decorators import superuser_required

from .models import Product, Category
from .forms import ProductForm, CategoryForm



def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)

    template = "product/product.html"
    context = {
        "config" : config,
        "product": product,
    }
    return render(request, template, context)


@login_required
@superuser_required
def products_view(request):
    user = request.user
    products = Product.objects.all()

    template = "product/admin/products.html"
    context = {
        'active': 'products',
        'config': config,
        'products': products 
    }
    return render(request, template, context)


@login_required
@superuser_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect(reverse('admin_product_update', args=[form.instance.id]))
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = ProductForm()

    template = "product/admin/product_add.html"
    context = {
        "form": form,
        'active': 'products'
    }
    return render(request, template, context)


@login_required
@superuser_required
def product_update_view(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = ProductForm(instance=product)

    template = "product/admin/product_update.html"
    context = {
        "product": product,
        "form": form,
        'active': 'products'
    }
    return render(request, template, context)


@login_required
@superuser_required
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
@superuser_required
def categories_view(request):
    user = request.user
    categories = Category.objects.all()

    template = "product/admin/categories.html"
    context = {
        'categories': categories,
        'active': 'categories'
    }

    return render(request, template, context)


@login_required
@superuser_required
def category_update_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = CategoryForm(instance=category)

    template = "product/admin/category_update.html"
    context = {
        "category": category,
        "form": form,
        'active': 'categories'
    }
    return render(request, template, context)


@login_required
@superuser_required
def category_delete_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        if category.id == 1:
            messages.error(request, 'You cannot delete the default category.')
            return redirect(reverse('admin_category_update', args=[category.id]))
        if category.product_set.count() > 0:
            messages.error(request, 'You cannot delete a category with products.')
            return redirect(reverse('admin_category_update', args=[category.id]))
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect(reverse('admin_categories'))
    
    template = "product/admin/categories.html"
    context = {
        "category": category,
        'active': 'categories'
    }
    return render(request, template, context)


@login_required
@superuser_required
def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect(reverse('admin_categories'))
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = CategoryForm()

    template = "product/admin/category_add.html"
    context = {
        "form": form,
        'active': 'categories'
    }
    return render(request, template, context)