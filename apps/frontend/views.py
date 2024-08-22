from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from constance import config
from .forms import ContactForm
from apps.product.models import Product, Category


def home(request):
    return render(request, "frontend/index.html")


def about(request):
    return render(request, "frontend/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            to_email = form.cleaned_data["email"]
            from_email = f'"Moodscape" <{settings.DEFAULT_FROM_EMAIL}>'
            subject = "Thank you for contacting Moodscape"

            admin_message = (
                "Thank you for reaching out! We have received "
                "your message and will get back to you soon."
            )
            user_message = form.cleaned_data["message"]

            message = (
                f"Dear {name}!\n\n{admin_message}\n\nHere is your "
                f"email:\n{user_message}\n\nMoodscape Team\n"
            )

            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )

            return redirect("contact_success")
    else:
        form = ContactForm()

    template = "frontend/contact.html"
    data = {
        "form": form,
    }
    return render(request, template, data)


def contact_success(request):
    template = "frontend/contact_success.html"
    return render(request, template)


def privacy(request):
    template = "frontend/privacy.html"
    return render(request, template)


def terms(request):
    template = "frontend/terms.html"
    return render(request, template)


def faq(request):
    template = "frontend/faq.html"
    return render(request, template)


def shop(request): 
    products = Product.objects.all()
    query = None
    category = None
    sort = None
    direction = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__slug=category)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.warning(request, "No search criteria provided")
            else:
                queries = Q(name__icontains=query) | Q(details__icontains=query)
                products = products.filter(queries)

        if 'sort' in request.GET:
            sort_option = request.GET['sort']
            sort = sort_option.split('_')[0]
            direction = sort_option.split('_')[1]

            if sort == 'alpha':
                sort = 'name_lower'
                products = products.annotate(name_lower=Lower('name'))
            elif sort == 'price':
                sort = 'price'
            elif sort == 'rating':
                sort = 'rating'

            if direction == 'desc':
                sort = f'-{sort}'

            products = products.order_by(sort)

    template = "frontend/shop.html"
    context = {
        "config": config,
        "products": products,
        "search_term": query,
        "category": category,
        "sort": f'{sort}_{direction}' if sort and direction else '',
    }
    return render(request, template, context)