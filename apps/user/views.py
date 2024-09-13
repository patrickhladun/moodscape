from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from constance import config

from apps.common.decorators import superuser_required

from .models import Customer
from .forms import AccountProfileForm, CustomerProfileForm

@login_required
@superuser_required
def cms_customers_view(request):
    customers = Customer.objects.all()

    template = "user/cms/customers.html"
    context = {
        'active': 'customers',
        'config': config,
        'customers': customers 
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_customer_update_view(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully.")
            return redirect('cms_customers')
    else:
        form = CustomerProfileForm(instance=customer)

    template = "user/cms/customer_update.html"
    context = {
        "active": "customers",
        "customer": customer,
        "form": form
    }
    return render(request, template, context)


@login_required
def account_view(request):
    user = request.user

    if request.method == "POST":
        form = AccountProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
        else:
            messages.error(request, "Please correct form errors.")
    else:
        form = AccountProfileForm(instance=user)

    template = "user/account/account.html"
    context = {
        'active': 'account',
        'form': form
    }
    return render(request, template, context)


@login_required
def account_profile_view(request):
    user = request.user
    customer = user.customer

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
    else:
        form = CustomerProfileForm(instance=customer)

    template = "user/account/profile.html"
    context = {
        'active': 'profile',
        'form': form
    }
    return render(request, template, context)