from decimal import Decimal

from constance import config
from django.shortcuts import get_object_or_404

from apps.product.models import Product


def bag_contents(request):
    """
    Calculates the contents of the shopping bag, including total cost, product
    count, and delivery charges.
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
            }
        )

    if total < config.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(config.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = config.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": config.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
