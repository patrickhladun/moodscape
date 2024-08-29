from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from constance import config

from apps.common.decorators import superuser_required

from .models import Customer
from .forms import AccountProfileForm

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
def account_view(request):
    user = request.user

    if request.method == "POST":
        form = AccountProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('account')
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

    if request.method == "POST":
        form = AccountProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('account_profile')
    else:
        form = AccountProfileForm(instance=user)

    template = "user/account/profile.html"
    context = {
        'active': 'profile'
    }
    return render(request, template, context)