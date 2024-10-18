import json

import stripe
from django.http import HttpResponse

from apps.checkout.emails import Emails
from apps.order.models import Order, OrderLineItem
from apps.product.models import Product


class Stripe_Webhook_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        This will create the order in the system if payment is successful.
        """
        intent = event.data.object
        charge = stripe.Charge.retrieve(intent.latest_charge)

        pid = intent.id
        bag = intent.metadata.bag
        username = intent.metadata.get("username")

        order = None
        try:
            order = Order.objects.get(stripe_pid=pid)

        except Order.DoesNotExist:
            order = None

        if not order:
            try:
                # Create a new order
                order = Order.objects.create(
                    first_name=billing_details.name.split(" ")[0],
                    last_name=billing_detailss.name.split(" ")[-1],
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=billing_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town_city=billing_details.address.city,
                    address_line_1=billing_details.address.line1,
                    address_line_2=billing_details.address.line2,
                    county=billing_details.address.state,
                    grand_total=grand_total,
                    stripe_pid=pid,
                )
                # Process each item in the bag and create order line items
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data[
                            "items_by_size"
                        ].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500,
                )

        email_handler = Emails()
        email_handler.send_confirmation_email(
            {
                "email": order.email,
                "order_number": order.order_number,
                "address_line_1": order.address_line_1,
                "town_city": order.town_city,
                "country": order.country,
            }
        )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )
