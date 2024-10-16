from constance import config
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.common.utils.metadata import make_metadata
from apps.product.models import Product


def bag_view(request):
    """
    Manages actions in the shopping bag page such as displaying items,
    removing them, or emptying the bag.
    """
    bag = request.session.get("bag", {})

    metadata = make_metadata(
        request,
        {
            "title": "Your Bag",
            "meta": {
                "description": "Review your selected items in your bag at \
                Moodscape. Modify quantities or proceed to checkout to \
                secure your unique art pieces."
            },
        },
    )

    if request.method == "POST":
        if "empty_bag" in request.POST:
            request.session["bag"] = {}
            messages.success(request, "Your cart is now empty.")
            return redirect("bag")
        elif "remove_item" in request.POST:
            product_id = request.POST.get("product_id")
            if product_id in bag:
                bag.pop(product_id)
                request.session["bag"] = bag
                messages.success(request, "Item removed from your cart.")
            else:
                messages.error(request, "Item not found in your cart.")
            return redirect("bag")
        elif "update_bag" in request.POST:
            product_id = request.POST.get("product_id")
            quantity = int(request.POST.get("quantity"))
            bag[product_id] = quantity
            request.session["bag"] = bag

    template = "bag/bag.html"
    context = {
        "config": config,
        "metadata": metadata,
    }
    return render(request, template, context)


def add_to_bag_view(request, id):
    """
    Adds a specified quantity of a product to the shopping bag or updates
    quantity if already in the bag.
    """
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})

    product = get_object_or_404(Product, pk=id)

    if id in bag:
        new_quantity = bag[id] + quantity
    else:
        new_quantity = quantity

    if product.stock == 0:
        messages.error(
            request,
            f"There is no {product.name} available in stock at the moment.",
        )
    elif new_quantity > product.stock:
        messages.error(
            request,
            f"Cannot add more than {product.stock} of {product.name} to your \
              cart.",
        )
    else:
        bag[id] = new_quantity
        messages.success(
            request, f"Added {quantity} of {product.name} to your cart."
        )

    request.session["bag"] = bag

    return redirect(redirect_url)


def remove_from_bag_view(request, id):
    """
    Removes a product from the shopping bag.
    """
    bag = request.session.get("bag", {})

    if id in bag:
        bag.pop(id)
        request.session["bag"] = bag
        messages.success(request, "Removed item from your cart.")
    else:
        messages.error(request, "Item not in your cart.")

    return redirect("bag:bag")
