from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from constance import config

from apps.product.models import Product

def bag_view(request):
    bag = request.session.get('bag', {})
    
    if request.method == 'POST':
        if 'empty_bag' in request.POST:
            request.session['bag'] = {}
            messages.success(request, "Your cart is now empty.")
            return redirect('bag')
        elif 'remove_item' in request.POST:
            product_id = request.POST.get('product_id')
            bag.pop(product_id)
            request.session['bag'] = bag
            messages.success(request, "Item removed from your cart.")
            return redirect('bag')
        elif 'update_bag' in request.POST:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity'))
            bag[product_id] = quantity
            request.session['bag'] = bag
            print(f"product_id: {product_id}, quantity: {quantity}")
            print(f"bag: {bag}")


    template = 'bag/bag.html'
    context = {
        'config': config,
    }
    return render(request, template, context)


def add_to_bag_view(request, id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    product = get_object_or_404(Product, pk=id)

    if id in bag:
        new_quantity = bag[id] + quantity
    else:
        new_quantity = quantity

    if new_quantity > product.stock:
        messages.error(request, f"Cannot add more than {product.stock} of {product.name} to your cart.")
    else:
        bag[id] = new_quantity
        messages.success(request, f"Added {quantity} of {product.name} to your cart.")

    request.session['bag'] = bag

    return redirect(redirect_url)


def remove_from_bag_view(request, id):
    bag = request.session.get('bag', {})

    if id in bag:
        bag.pop(id)
        request.session['bag'] = bag
        messages.success(request, "Removed item from your cart.")
    else:
        messages.error(request, "Item not in your cart.")

    return redirect('bag:bag')
