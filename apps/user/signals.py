from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer

@receiver(post_save, sender=User)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    """
    Automatically create a Customer for new Users,
    but only if a Customer doesn't already exist.
    """
    if created:
        # Ensure a Customer doesn't already exist for this User
        if not hasattr(instance, "customer"):
            Customer.objects.create(user=instance)
