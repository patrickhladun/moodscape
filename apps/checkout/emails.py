from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Emails:
    def __init__(self):
        pass

    def send_confirmation_email(self, order):
        """Send the user a confirmation email with HTML content"""
        try:
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = order["email"]
            subject = (
                f"Confirmation for Order Number {order['order_number']}"
            )

            html = render_to_string(
                "checkout/emails/confirmation_email.html", {"order": order}
            )
            text = render_to_string(
                "checkout/emails/confirmation_email.txt", {"order": order}
            )

            email = EmailMultiAlternatives(
                subject, text, email_from, [email_to]
            )
            email.attach_alternative(html, "text/html")

            email.send()
        except Exception as e:
            print(f"An error occurred in send_confirmation_email: {e}")
