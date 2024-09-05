from django.db import models
from apps.product.models import Product
from apps.order.models import OrderLineItem
from apps.user.models import User

class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted'),
    ]

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, related_name="user_reviews", on_delete=models.CASCADE)
    order_line_item = models.ForeignKey(OrderLineItem, on_delete=models.CASCADE, related_name='lineitem_reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField(max_length=160)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mood_reviews'
        unique_together = ('order_line_item', 'user')

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
        
