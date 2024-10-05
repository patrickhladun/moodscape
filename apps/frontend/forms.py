from django import forms


class ContactForm(forms.Form):
    """
    Form for users to submit contact information and a message.
    """

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class NewsletterForm(forms.Form):
    subscriber_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "bg-blue-800 text-blue-50 w-full py-2 px-4 m-0 rounded-l-lg border-none focus:ring-0",
                "placeholder": "Enter your best email",
                "aria-label": "Email Address",
            }
        )
    )
