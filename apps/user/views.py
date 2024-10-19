from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.common.decorators import superuser_required
from apps.common.utils.metadata import make_metadata

from .forms import AccountProfileForm, CustomerProfileForm
from .models import Customer


@superuser_required
def cms_customers_view(request):
    """
    Retrieves and displays a list of all registered customers to superusers,
    allowing for management actions such as viewing, editing, or contacting
    customers.
    """
    customers = Customer.objects.all()

    metadata = make_metadata(
        request,
        {
            "title": "Customer List",
            "meta": {
                "description": (
                    "View and manage all registered customers. Access "
                    "customer profiles, edit information, or initiate contact "
                    "directly from this list."
                )
            },
        },
    )

    template = "user/cms/customers.html"
    context = {
        "active": "customers",
        "config": config,
        "metadata": metadata,
        "customers": customers,
    }
    return render(request, template, context)


@superuser_required
def cms_customer_update_view(request, id):
    """
    Provides a form for superusers to update the details of a specific
    customer, including personal and contact information, from the CMS panel.
    """
    customer = get_object_or_404(Customer, id=id)

    metadata = make_metadata(
        request,
        {
            "title": (
                "Update Customer "
                f"- {customer.first_name} {customer.last_name}"
            ),
            "meta": {
                "description": (
                    "Update personal and contact details for "
                    f"{customer.first_name} {customer.last_name}. This page "
                    "allows for comprehensive management of customer "
                    "information."
                )
            },
        },
    )

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Customer details updated successfully."
            )
            return redirect("cms_customers")
    else:
        form = CustomerProfileForm(instance=customer)

    template = "user/cms/customer_update.html"
    context = {
        "active": "customers",
        "metadata": metadata,
        "customer": customer,
        "form": form,
    }
    return render(request, template, context)


@superuser_required
def cms_customer_delete_view(request, id):
    """
    Allows superusers to delete a customer's profile from the CMS panel.
    This action is irreversible and removes the customer from the database.
    """
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect("cms_customers")

    return redirect("cms_customers")


@login_required
def account_view(request):
    """
    Provides a view for logged-in users to update their account settings,
    such as email and password, ensuring their personal details are current
    and secure.
    """
    user = request.user

    metadata = make_metadata(
        request,
        {
            "title": "Account Settings",
            "meta": {
                "description": (
                    "Adjust your account settings, including email "
                    "and password."
                )
            },
        },
    )

    if request.method == "POST":
        form = AccountProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account details updated successfully."
            )
        else:
            messages.error(request, "Please correct form errors.")
    else:
        form = AccountProfileForm(instance=user)

    template = "user/account/account.html"
    context = {"active": "account", "metadata": metadata, "form": form}
    return render(request, template, context)


@login_required
def account_profile_view(request):
    """
    Enables users to view and update their personal profile information, such
    as name and contact details, ensuring that their profile reflects accurate
    and up-to-date information.
    """
    user = request.user
    customer = user.customer

    metadata = make_metadata(
        request,
        {
            "title": "Your Profile",
            "meta": {
                "description": (
                    "Manage your personal information and preferences."
                )
            },
        },
    )

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account details updated successfully."
            )
    else:
        form = CustomerProfileForm(instance=customer)

    template = "user/account/profile.html"
    context = {"active": "profile", "metadata": metadata, "form": form}
    return render(request, template, context)
