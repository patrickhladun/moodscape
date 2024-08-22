from django.shortcuts import render

def checkout_view(request):

    template = 'checkout/checkout.html'
    context = {}
    return render(request, template, context)


def checkout_success_view(request):

    template = 'checkout/checkout_success.html'
    context = {}
    return render(request, template, context)


