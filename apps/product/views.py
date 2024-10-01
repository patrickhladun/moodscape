from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from constance import config
from apps.common.decorators import superuser_required
from apps.common.utils.metadata import make_metadata

from .models import Product, Category
from .forms import ProductForm, CategoryForm



def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.filter(status='approved')

    stock = "in stock" if product.stock > 0 else "out of stock"

    metadata = make_metadata(
        request,
        {
            "title": product.name,
            "meta": {
                "description": product.meta_desc,
            },
            "og": {
                "image": product.featured.url,
            },
            "twitter": {
                "image": product.featured.url,
            },
            "product": {
                "sku": product.sku,
                "price": product.price,
                "availability": stock,
                "condition": "new",
                "brand": config.SITE_NAME,
                "category": product.category.name,
                "image": product.featured.url,
            }
        },
    )

    template = "product/product.html"
    context = {
        "config" : config,
        "active": "shop",
        "product": product,
        "reviews": reviews,
        "metadata": metadata,
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_products_view(request):
    user = request.user
    products = Product.objects.all()

    metadata = make_metadata(
        request,
        {
            "title": "Products List",
            "meta": {
                "description": "Browse the complete catalog of products available on Moonscape. This page provides an overview of all products, allowing for easy management and access to product details."
            }
        },
    )

    template = "product/cms/products.html"
    context = {
        'active': 'products',
        'config': config,
        'metadata': metadata,
        'products': products 
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_product_add_view(request):

    metadata = make_metadata(
    request,
        {
            "title": "Add New Product",
            "meta": {
                "description": "Add a new product to Moonscape's catalog. Specify product details such as name, price, and category to introduce new art pieces to the shop."
            }
        },
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect(reverse('cms_product_update', args=[form.instance.id]))
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = ProductForm()

    template = "product/cms/product_add.html"
    context = {
        'active': 'products',
        'metadata': metadata,
        'form': form,
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_product_update_view(request, id):
    product = get_object_or_404(Product, id=id)

    metadata = make_metadata(
        request,
        {
            "title": f"Update Product - {product.name}",
            "meta": {
                "description": f"Update existing product details for {product.name}. This page allows for the modification of price, stock levels, and other critical product information."
            }
        },
    )
    
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

    template = "product/cms/product_update.html"
    context = {
        'active': 'products',
        'metadata': metadata,
        "product": product,
        "form": form,
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_product_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect(reverse('cms_products'))
    
    template = "product/cms/products.html"
    context = {
        "product": product,
        'active': 'products'
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_categories_view(request):
    user = request.user
    categories = Category.objects.all()
    
    metadata = make_metadata(
        request,
        {
            "title": "Categories List",
            "meta": {
                "description": "View and manage all categories on Moonscape. This administrative page provides an overview of all categories, facilitating the organization of products."
            }
        },
    )

    template = "product/cms/categories.html"
    context = {
        'active': 'categories',
        'metadata': metadata,
        'categories': categories,
    }

    return render(request, template, context)


@login_required
@superuser_required
def cms_category_update_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    metadata = make_metadata(
        request,
        {
            "title": f"Update Category - {category.name}",
            "meta": {
                "description": f"Edit the details of the {category.name} category. This page allows for the modification of category names and descriptions to better align with the evolving inventory."
            }
        },
    )

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

    template = "product/cms/category_update.html"
    context = {
        'active': 'categories',
        'metadata': metadata,
        'category': category,
        'form': form
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_category_delete_view(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        if category.id == 1:
            messages.error(request, 'You cannot delete the default category.')
            return redirect(reverse('cms_category_update', args=[category.id]))
        if category.product_set.count() > 0:
            messages.error(request, 'You cannot delete a category with products.')
            return redirect(reverse('cms_category_update', args=[category.id]))
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect(reverse('cms_categories'))
    
    template = "product/cms/categories.html"
    context = {
        "category": category,
        'active': 'categories'
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_category_add_view(request):

    metadata = make_metadata(
        request,
        {
            "title": "Add New Category",
            "meta": {
                "description": "Create a new category for organizing products on Moonscape. This page allows administrators to define new categories that will help structure the site's offerings."
            }
        },
    )

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect(reverse('cms_categories'))
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join([field for field, _ in form.errors.items()])
            messages.error(request, error_message + error_fields)
    else:
        form = CategoryForm()

    template = "product/cms/category_add.html"
    context = {
        'active': 'categories',
        'metadata': metadata,
        'form': form,
    }
    return render(request, template, context)