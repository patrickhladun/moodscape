from .forms import NewsletterForm


def newsletter_form(request):
    """
    Context processor to inject the newsletter form into the template context.
    This allows the newsletter form to be available and rendered on any page.
    """
    return {"newsletter_form": NewsletterForm()}
