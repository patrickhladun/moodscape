from django import forms
from .models import User, Customer


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username"]


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "town_city",
            "county",
            "country",
            "postcode",
        ]
