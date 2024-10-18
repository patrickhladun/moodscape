from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Emails:
    def __init__(self):
        pass

    def send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        try:
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = order["email"]
            subject = (
                f"Confirmation for Order Number {order['order_number']}"
            )
            body = f"Thank you for your order {order['order_number']}! Your order will be shipped to {order['address_line_1']} {order['town_city']}, {order['country']}."

            send_mail(subject, body, email_from, [email_to])
        except Exception as e:
            print(f"An error occurred in send_confirmation_email: {e}")
