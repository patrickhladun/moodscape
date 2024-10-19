from django import forms
from django.utils.text import slugify
from django_summernote.widgets import SummernoteWidget

from .models import Category, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "details",
            "sku",
            "stock",
            "price",
            "featured",
            "category",
            "is_published",
        ]
        widgets = {
            "details": SummernoteWidget(),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        name = self.cleaned_data.get("name")

        if not slug:
            slug = slugify(name)

        queryset = Product.objects.filter(slug=slug).exclude(
            id=self.instance.id
        )
        if queryset.exists():
            raise forms.ValidationError(
                (
                    "A product with this slug already exists. Please choose a "
                    "different name or provide a unique slug."
                )
            )

        return slug

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0 or price == 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]
