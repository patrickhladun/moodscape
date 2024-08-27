import re
from django import forms
from django.core.exceptions import ValidationError
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
            'email': 'Email',
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


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if not re.match(r'^[a-zA-Z\s-]+$', first_name):
            raise ValidationError('First name can only contain letters, spaces, and hyphens.')

        return first_name
        

    def clean_country(self):
        country = self.cleaned_data.get('country')

        if not country or country.strip() == '':
            raise ValidationError('Please select a valid country.')

        return country


class UpdateOrderForm(forms.ModelForm):
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


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['product', 'quantity']


class AddOrderItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(min_value=1, required=True)


class UpdateOrderStatusForm(forms.Form):
    status_choices = [
        ('cancelled', 'Cancelled'),
        ('complete', 'Complete'),
        ('processing', 'Processing'),
    ]
    status = forms.ChoiceField(choices=status_choices, required=True)