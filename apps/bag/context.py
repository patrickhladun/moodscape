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
    delivery = 0
    bag = request.session.get("bag", {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        item_total = quantity * product.price
        total += item_total
        product_count += quantity
        bag_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
                "subtotal": item_total,
            }
        )

    if total > config.FREE_DELIVERY_THRESHOLD:
        delivery = 0
    else:
        delivery = product_count * Decimal(config.STANDARD_DELIVERY_PER_ITEM)

    grand_total = total + delivery

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "grand_total": grand_total,
    }

    return context
