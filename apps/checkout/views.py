from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from allauth.account.forms import SignupForm
from constance import config

from apps.order.forms import CreateOrderForm
from apps.order.models import Order, OrderLineItem
from apps.bag.context import bag_contents
from apps.product.models import Product
from apps.user.models import User, Customer
from apps.common.utils.metadata import make_metadata

import stripe

def checkout_view(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    metadata = make_metadata(
        request,
        {
            "title": "Checkout",
            "meta": {
                "description": "Complete your purchase on Moonscape. Securely enter your shipping and payment details to finalize your order of unique art pieces."
            }
        },
    )

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        create_account = request.POST.get('create_account', False)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        address = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_city': request.POST['town_city'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'county': request.POST['county'],
        }

        form_data = {
            'email': request.POST['email'],
            **address
        }

        order_form = CreateOrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()

            if create_account:
                if password == confirm_password:
                    user = User.objects.create_user(
                        username=request.POST['email'],
                        email=request.POST['email'],
                        password=password
                    )

                    customer = Customer.objects.create(
                        user=user,
                        **address
                    )

                    order.customer = customer
                    order.save()

                else:
                    messages.error(request, "Passwords do not match.")
                    return redirect(reverse('checkout'))

            for item_id, quantity in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))                
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

        # If it's a POST request, we don't need to generate a Stripe payment intent
        client_secret = ''
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('shop'))

        # Pre-populate form if the user is logged in
        if request.user.is_authenticated:
            try:
                customer = request.user.customer  # Assuming you have a customer relationship
                initial_data = {
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'phone_number': customer.phone_number,
                    'country': customer.country,
                    'postcode': customer.postcode,
                    'town_city': customer.town_city,
                    'address_line_1': customer.address_line_1,
                    'address_line_2': customer.address_line_2,
                    'county': customer.county,
                    'email': request.user.email
                }
            except AttributeError:
                # If there's no Customer record, use only the user email
                initial_data = {'email': request.user.email}
        else:
            initial_data = {}

        order_form = CreateOrderForm(initial=initial_data)

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=config.CURRENCY,
        )

        client_secret = intent.client_secret

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        "config": config,
        "metadata": metadata,
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,  # Pass an empty client_secret if it's a POST request
    }
    return render(request, template, context)




def checkout_success_view(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    metadata = make_metadata(
        request,
        {
            "title": "Thank You",
            "meta": {
                "description": "Thank you for your purchase at Moonscape! Check your email for order details and shipping confirmation. We hope you enjoy your new art pieces."
            },
        },
    )
    
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        "metadata": metadata,
        'order': order,
    }

    return render(request, template, context)


