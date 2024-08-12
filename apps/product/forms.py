from django import forms
from django.utils.text import slugify
from .models import Product, Category
from django_summernote.widgets import SummernoteWidget

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'details', 'sku', 'stock', 'price', 'featured', 'category', 'is_published']
        widgets = {
            'details': SummernoteWidget(),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        name = self.cleaned_data.get('name')
        
        if not slug:
            slug = slugify(name)
        
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A product with this slug already exists. Please choose a different name or provide a unique slug.")

        return slug


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'featured', 'price', 'slug', 'details', 'stock', 'sku', 'featured', 'is_published', 'category']
        widgets = {
            'details': SummernoteWidget(),
        }