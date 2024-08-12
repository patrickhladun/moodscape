from django import forms
from .models import Product, Category

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'featured', 'price', 'slug', 'details', 'stock', 'sku', 'featured', 'is_draft', 'category']