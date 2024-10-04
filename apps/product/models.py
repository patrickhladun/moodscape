import os
import random
import string
from datetime import datetime
from django.db import models
from apps.user.models import User


def featured_image_path(instance, filename):
    """
    Generate a file upload path with a random four-character string and the product ID in the filename.
    """
    timestamp = datetime.now().strftime("%y%m%d")
    extension = os.path.splitext(filename)[1]
    rand_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    new_filename = f"featured_{timestamp}_{rand_chars}{extension}"
    path = "products/"
    return os.path.join(path, new_filename)



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    meta_desc = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    details = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=255, unique=True)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, null=True, blank=True)
    featured = models.ImageField(upload_to=featured_image_path, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mood_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mood_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
