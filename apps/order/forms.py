from django import forms
from .models import Order, OrderLineItem
from apps.product.models import Product

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'email',
            'first_name',
            'last_name', 
            'phone_number',
            'address_line_1', 
            'address_line_2',
            'town_city', 
            'postcode', 
            'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'town_city': 'Town or City',
            'postcode': 'Postcode',
            'country': 'Country',
            'county': 'County',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
    
        
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


