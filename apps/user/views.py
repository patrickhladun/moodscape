from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AccountProfileForm


@login_required
def account_view(request):
    user = request.user

    if request.method == "POST":
        form = AccountProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('user_account')
    else:
        form = AccountProfileForm(instance=user)

    template = "user/admin/account.html"
    context = {
        'form': form,
    }
    return render(request, template, context)