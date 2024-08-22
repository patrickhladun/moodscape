from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order


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