from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm

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