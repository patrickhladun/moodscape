from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.common.decorators import superuser_required
from constance import config
from apps.common.utils.metadata import make_metadata

from .models import Order, OrderLineItem
from apps.review.models import Review
from .forms import UpdateOrderForm, OrderStatusForm, AddOrderItemForm, OrderItemForm


@login_required
@superuser_required
def cms_order_update_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    metadata = make_metadata(
        request,
        {
            "title": f"Order Details - {order.order_number}",
            "meta": {
                "description": f"Review and manage details for order {order.order_number}. Update statuses, manage items, and view customer shipping information."
            }
        },
    )

    if request.method == 'POST':
        if 'update_status' in request.POST:
            status_form = OrderStatusForm(request.POST, instance=order)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Order status updated successfully.')
                return redirect(reverse('cms_order_update', args=[order_number]))
        elif 'update_form' in request.POST:
            update_form = UpdateOrderForm(request.POST, instance=order)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Order updated successfully.')
                return redirect(reverse('cms_order_update', args=[order_number]))
        elif 'add_item' in request.POST:
            add_form = AddOrderItemForm(request.POST)
            if add_form.is_valid():
                product = add_form.cleaned_data['product']
                quantity = add_form.cleaned_data['quantity']
                OrderLineItem.objects.create(order=order, product=product, quantity=quantity)
                order.update_total()
                messages.success(request, 'Item added successfully.')
                return redirect(reverse('cms_order_update', args=[order_number]))
        elif 'update_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(OrderLineItem, id=item_id, order=order)
            item_form = OrderItemForm(request.POST, instance=item)
            if item_form.is_valid():
                item_form.save()
                order.update_total()
                messages.success(request, 'Item updated successfully.')
                return redirect(reverse('cms_order_update', args=[order_number]))
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(OrderLineItem, id=item_id, order=order)
            item.delete()
            order.update_total()
            messages.success(request, 'Item deleted successfully.')
            return redirect(reverse('cms_order_update', args=[order_number]))
    else:
        status_form = OrderStatusForm(instance=order)
        update_form = UpdateOrderForm(instance=order)
        add_form = AddOrderItemForm()
        item_forms = [OrderItemForm(instance=item) for item in order.lineitems.all()]

    context = {
        'active': 'orders',
        'metadata': metadata,
        'order': order,
        'status_form': status_form,
        'update_form': update_form,
        'add_form': add_form,
        'item_forms': item_forms,
    }

    return render(request, 'order/cms/order_update.html', context)


@login_required
@superuser_required
def cms_orders_view(request):
    orders = Order.objects.all()

    metadata = make_metadata(
        request,
        {
            "title": "Admin Orders",
            "meta": {
                "description": "Manage and review all placed orders on Moonscape. Track order status, view customer details, and update order information effectively."
            }
        },
    )
    
    template = 'order/cms/orders.html'
    context = {
        'active': 'orders',
        'metadata': metadata,
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def account_orders_view(request):
    orders = Order.objects.all()

    metadata = make_metadata(
        request,
        {
            "title": "Your Orders",
            "meta": {
                "description": "View your order history and track current orders."
            }
        },
    )
    
    template = 'order/account/orders.html'
    context = {
        'active': 'orders',
        'metadata': metadata,
        'config': config,
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def account_order_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.lineitems.all()

    metadata = make_metadata(
        request,
        {
            "title": "Order Details",
            "meta": {
                "description": "Detailed view of your specific order."
            }
        },
    )

    for item in items:
        item.reviewed = Review.objects.filter(order_line_item=item, user=request.user).exists()

    order.items = items
    template = 'order/account/order.html'
    context = {
        'active': 'orders',
        'metadata': metadata,
        'order': order,
        'config': config,
    }
    return render(request, template, context)