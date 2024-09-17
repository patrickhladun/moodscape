from django import forms


class ContactForm(forms.Form):
    """
    Form for users to submit contact information and a message.
    """

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)