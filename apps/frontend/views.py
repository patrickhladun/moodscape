import requests
from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse

from apps.common.decorators import superuser_required
from apps.common.utils.metadata import make_metadata
from apps.product.models import Category, Product

from .forms import ContactForm, FAQForm, FAQSectionForm, NewsletterForm
from .models import FAQ, FAQSection, ContactMessage


def home(request):
    """
    Renders the home page with featured products and sets page metadata.
    """
    product_ids = [7, 23, 52, 86]
    featured = Product.objects.filter(id__in=product_ids)

    metadata = make_metadata(
        request,
        {
            "title": "Unique Watercolor & Abstract Art",
            "meta": {
                "description": "Explore Moodscape, an e-commerce platform \
                offering unique watercolor art, Irish abstract landscapes, \
                and pen plotter art. Beautify your space with stunning art \
                pieces.",
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
    """
    Renders the about page with company information and sets page metadata.
    """
    metadata = make_metadata(
        request,
        {
            "title": "About Us",
            "meta": {
                "description": "Learn more about Moodscape, an online art \
                platform providing curated collections of watercolor art, \
                abstract landscapes, floral art, and digital photography.",
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
    """
    Handles contact form submissions and renders the contact page.
    If the form is valid, saves the contact message, sends an email, and
    redirects to a success page.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Contact Us",
            "meta": {
                "description": "Get in touch with the Moodscape Art team for \
                inquiries, support, or questions about your order. We are \
                here to assist with any art-related queries.",
            },
        },
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            ContactMessage.objects.create(
                name=name, email=email, message=message
            )

            from_email = f'"Moodscape" <{settings.DEFAULT_FROM_EMAIL}>'
            subject = "Thank you for contacting Moodscape"
            user_message = form.cleaned_data["message"]

            message = (
                f"Dear {name}!\n\n"
                "Thank you for reaching out! We have received "
                "your message and will get back to you soon.\n\n"
                "Here is your message:\n"
                f"{user_message}\n\n"
                "Moodscape Team\n"
            )

            send_mail(
                subject,
                message,
                from_email,
                [email],
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
    """
    Renders the privacy policy page and sets page metadata.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Privacy Policy | Moodscape Art",
            "meta": {
                "description": "Read Moodscape's privacy policy to understand \
                how we collect, use, and protect your personal \
                information while you browse and shop on our platform.",
            },
        },
    )

    template = "frontend/privacy.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


def terms(request):
    """
    Renders the terms and conditions page and sets page metadata.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Terms and Conditions | Moodscape Art",
            "meta": {
                "description": "Review Moodscape's terms and conditions for \
                using our e-commerce platform, including details about \
                purchases, payments, and user responsibilities.",
            },
        },
    )

    template = "frontend/terms.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


def faq(request):
    """
    Renders the FAQ page, providing answers to common questions and sets
    page metadata.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Frequently Asked Questions (FAQ) | Moodscape Art",
            "meta": {
                "description": "Find answers to common questions about \
                Moodscape's products, shipping, payments, returns, and more \
                in our FAQ section.",
            },
        },
    )

    # Fetch all sections with their FAQs
    sections = FAQSection.objects.prefetch_related("faq_set")

    template = "frontend/faq.html"
    context = {
        "metadata": metadata,
        "sections": sections,
    }
    return render(request, template, context)


def shop(request):
    """
    Renders the shop page with filterable and sortable product listings based
    on user input. Sets metadata for the shop page.
    """
    products = Product.objects.all()
    query = None
    category = None
    sort = None
    direction = None

    metadata = make_metadata(
        request,
        {
            "title": "Shop Art | Moodscape Art",
            "meta": {
                "description": "Browse and shop unique watercolor art, Irish \
                abstract landscapes, floral art, pen plotter art, and digital \
                photography at Moodscape Art.",
            },
        },
    )

    if request.GET:
        if "category" in request.GET:
            category = request.GET["category"]
            products = products.filter(category__slug=category)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.warning(request, "No search criteria provided")
            else:
                queries = Q(name__icontains=query) | Q(
                    details__icontains=query
                )
                products = products.filter(queries)

        if "sort" in request.GET:
            sort_option = request.GET["sort"]
            sort = sort_option.split("_")[0]
            direction = sort_option.split("_")[1]

            if sort == "alpha":
                sortfield = "name_lower"
                products = products.annotate(name_lower=Lower("name"))
            elif sort == "price":
                sortfield = "price"
            elif sort == "rating":
                sortfield = "rating"
            else:
                sortfield = "id"

            if direction == "desc":
                sortfield = f"-{sortfield}"

            products = products.order_by(sortfield)
        else:
            sort_option = ""

    else:
        sort_option = ""

    context = {
        "config": config,
        "active": "shop",
        "metadata": metadata,
        "products": products,
        "search_term": query,
        "category": category,
        "sort": sort_option,
    }
    return render(request, "frontend/shop.html", context)


def newsletter_subscribe(request):
    """
    Handles newsletter subscription requests. Submits the subscriber's email
    to a third-party service and redirects to a success page or shows an
    error message.
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["subscriber_email"]
            form_id = "7110513"
            api_key = "lJ2VYug5Dns_a4kWThvbWg"
            try:
                response = requests.post(
                    f"https://api.convertkit.com/v3/forms/{form_id}/subscribe",
                    data={"email": email, "api_key": api_key},
                )
                response.raise_for_status()
                return redirect("success_newsletter")
            except requests.RequestException:
                messages.error(
                    request, "Failed to subscribe. Please try again later."
                )
    else:
        for error in form.errors.values():
            messages.error(request, error)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def success_newsletter(request):
    """
    Renders the newsletter subscription success page and sets page metadata.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Subscription Newsletter",
            "meta": {
                "description": "Thank you for subscribing to Moodscape's \
                newsletter. Please check your email to confirm your \
                subscription and start receiving updates.",
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
    """
    Renders the contact form success page after a user has successfully
    submitted a message.
    """
    metadata = make_metadata(
        request,
        {
            "title": "Message Sent",
            "meta": {
                "description": "Thank you for contacting Moodscape. Your \
                message has been successfully sent, and we will get back to \
                you shortly.",
                "robots": "noindex, nofollow",
            },
        },
    )

    template = "frontend/success_contact.html"
    context = {
        "metadata": metadata,
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_faqs_view(request):
    """
    Renders the FAQ page in the CMS, allowing admin users to manage and
    update the FAQ content.
    """
    faqs = FAQ.objects.all()

    metadata = make_metadata(
        request,
        {
            "title": "FAQ",
            "meta": {
                "description": "Manage and update the FAQ content on the \
                Moodscape platform. Provide answers to common questions about \
                products, shipping, payments, and more.",
            },
        },
    )

    template = "frontend/cms/faqs.html"
    context = {
        "metadata": metadata,
        "active": "faqs",
        "faqs": faqs,
    }
    return render(request, template, context)


@login_required
@superuser_required
def cms_faqs_add_view(request):
    """
    Handles the addition of a new FAQ entry in the CMS.
    """

    metadata = make_metadata(
        request,
        {
            "title": "FAQ",
            "meta": {
                "description": "Manage and update the FAQ content on the \
                Moodscape platform. Provide answers to common questions about \
                products, shipping, payments, and more.",
            },
        },
    )

    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ item added successfully.")
            return redirect(reverse("cms_faqs"))
        else:
            error_message = "You have errors in the following fields: "
            error_fields = ", ".join(
                [field for field, _ in form.errors.items()]
            )
            messages.error(request, error_message + error_fields)
    else:
        form = FAQForm()

    template = "frontend/cms/faqs_add.html"
    context = {
        "metadata": metadata,
        "active": "faqs",
        "form": form,
    }
    return render(request, template, context)

