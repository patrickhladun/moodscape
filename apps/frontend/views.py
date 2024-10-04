import requests
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.http import HttpResponseRedirect
from constance import config
from .forms import ContactForm, NewsletterForm
from apps.product.models import Product, Category
from apps.common.utils.metadata import make_metadata


def home(request):
    product_ids = [7, 23, 52, 86]
    featured = Product.objects.filter(id__in=product_ids)

    metadata = make_metadata(
        request,
        {
            "title": "Unique Watercolor & Abstract Art",
            "meta": {
                "description": "Explore Moonscape, an e-commerce platform offering unique watercolor art, Irish abstract landscapes, and pen plotter art. Beautify your space with stunning art pieces.",
            },
        },
    )
    
    template = "frontend/index.html"
    context = {
        "metadata": metadata,
        "featured": featured,
    }
    return render(request, template, context)


def about(request):
    metadata = make_metadata(
        request,
        {
            "title": "About Us",
            "meta": {
                "description": "Learn more about Moonscape, an online art platform providing curated collections of watercolor art, abstract landscapes, floral art, and digital photography.",
            },
        },
    )

    template = "frontend/about.html"
    context = {
        "active": "about",
        "metadata": metadata,
    }
    return render(request, template, context)


def contact(request):
    metadata = make_metadata(
        request,
        {
            "title": "Contact Us",
            "meta": {
                "description": "Get in touch with the Moonscape Art team for inquiries, support, or questions about your order. We are here to assist with any art-related queries.",
            },
        },
    )

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

            return redirect("success_contact")
    else:
        form = ContactForm()

    template = "frontend/contact.html"
    context = {
        "active": "contact",
        "form": form,
        "metadata": metadata,
    }
    return render(request, template, context)


def privacy(request):
    metadata = make_metadata(
        request,
        {
            "title": "Privacy Policy | Moonscape Art",
            "meta": {
                "description": "Read Moonscape's privacy policy to understand how we collect, use, and protect your personal information while you browse and shop on our platform.",
            },
        },
    )

    template = "frontend/privacy.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


def terms(request):
    metadata = make_metadata(
        request,
        {
            "title": "Terms and Conditions | Moonscape Art",
            "meta": {
                "description": "Review Moonscape's terms and conditions for using our e-commerce platform, including details about purchases, payments, and user responsibilities.",
            },
        },
    )

    template = "frontend/terms.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


def faq(request):
    metadata = make_metadata(
        request,
        {
            "title": "Frequently Asked Questions (FAQ) | Moonscape Art",
            "meta": {
                "description": "Find answers to common questions about Moonscape's products, shipping, payments, returns, and more in our FAQ section.",
            },
        },
    )

    template = "frontend/faq.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


def shop(request): 
    products = Product.objects.all()
    query = None
    category = None
    sort = None
    direction = None

    metadata = make_metadata(
        request,
        {
            "title": "Shop Art | Moonscape Art",
            "meta": {
                "description": "Browse and shop unique watercolor art, Irish abstract landscapes, floral art, pen plotter art, and digital photography at Moonscape Art.",
            },
        },
    )

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
        "active": "shop",
        "metadata": metadata,
        "products": products,
        "search_term": query,
        "category": category,
        "sort": f'{sort}_{direction}' if sort and direction else '',
    }
    return render(request, template, context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['subscriber_email']
            form_id = '7110513'
            api_key = 'lJ2VYug5Dns_a4kWThvbWg'
            try:
                response = requests.post(
                    f'https://api.convertkit.com/v3/forms/{form_id}/subscribe',
                    data={'email': email, 'api_key': api_key}
                )
                response.raise_for_status()
                return redirect('success_newsletter')
            except requests.RequestException:
                messages.error(request, 'Failed to subscribe. Please try again later.')
    else:
        for error in form.errors.values():
                messages.error(request, error)
    return redirect(request.META.get('HTTP_REFERER', '/'))



def success_newsletter(request):
    metadata = make_metadata(
        request,
        {
            "title": "Subscription Newsletter",
            "meta": {
                "description": "Thank you for subscribing to Moonscape's newsletter. Please check your email to confirm your subscription and start receiving updates.",
            },
        },
    )

    template = "frontend/success_newsletter.html"
    context = {
        "active": "contact",
        "metadata": metadata,
    }
    return render(request, template, context)


def success_contact(request):
    metadata = make_metadata(
        request,
        {
            "title": "Message Sent",
            "meta": {
                "description": "Thank you for contacting Moonscape. Your message has been successfully sent, and we will get back to you shortly.",
                "robots": "noindex, nofollow",
            },
        },
    )

    template = "frontend/success_contact.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)