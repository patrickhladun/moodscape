from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

from apps.review.models import Review
from .models import Product

def update_product_rating(product):
    """ Helper function to update the product's rating. """
    new_rating = Review.objects.filter(product=product, status='approved').aggregate(Avg('rating'))['rating__avg']
    product.rating = round(new_rating, 1) if new_rating else None
    product.save(update_fields=['rating'])

@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, created, **kwargs):
    """ Update the product rating if a review's approval status changes. """
    if instance.status == 'approved' or (not created and 'status' in instance.tracker.changed()):
        update_product_rating(instance.product)

@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    """ Update the product rating when an approved review is deleted. """
    if instance.status == 'approved':
        update_product_rating(instance.product)
