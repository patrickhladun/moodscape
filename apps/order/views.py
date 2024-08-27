from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.common.decorators import superuser_required

from .models import Order, OrderLineItem
from .forms import UpdateOrderForm, OrderStatusForm, AddOrderItemForm, OrderItemForm


@login_required
@superuser_required
def order_update_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if request.method == 'POST':
        if 'update_status' in request.POST:
            status_form = OrderStatusForm(request.POST, instance=order)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Order status updated successfully.')
                return redirect(reverse('admin_order_update', args=[order_number]))
        elif 'update_form' in request.POST:
            update_form = UpdateOrderForm(request.POST, instance=order)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Order updated successfully.')
                return redirect(reverse('admin_order_update', args=[order_number]))
        elif 'add_item' in request.POST:
            add_form = AddOrderItemForm(request.POST)
            if add_form.is_valid():
                product = add_form.cleaned_data['product']
                quantity = add_form.cleaned_data['quantity']
                OrderLineItem.objects.create(order=order, product=product, quantity=quantity)
                order.update_total()
                messages.success(request, 'Item added successfully.')
                return redirect(reverse('admin_order_update', args=[order_number]))
        elif 'update_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(OrderLineItem, id=item_id, order=order)
            item_form = OrderItemForm(request.POST, instance=item)
            if item_form.is_valid():
                item_form.save()
                order.update_total()
                messages.success(request, 'Item updated successfully.')
                return redirect(reverse('admin_order_update', args=[order_number]))
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(OrderLineItem, id=item_id, order=order)
            item.delete()
            order.update_total()
            messages.success(request, 'Item deleted successfully.')
            return redirect(reverse('admin_order_update', args=[order_number]))
    else:
        status_form = OrderStatusForm(instance=order)
        update_form = UpdateOrderForm(instance=order)
        add_form = AddOrderItemForm()
        item_forms = [OrderItemForm(instance=item) for item in order.lineitems.all()]

    context = {
        'active': 'orders',
        'order': order,
        'status_form': status_form,
        'update_form': update_form,
        'add_form': add_form,
        'item_forms': item_forms,
    }

    return render(request, 'order/admin/order_update.html', context)


@login_required
@superuser_required
def orders_view(request):
    orders = Order.objects.all()
    
    template = 'order/admin/orders.html'
    context = {
        'active': 'orders',
        'orders': orders,
    }
    return render(request, template, context)