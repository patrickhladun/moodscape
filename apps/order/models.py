import uuid
from decimal import Decimal

from constance import config
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from django_countries.fields import CountryField

from apps.product.models import Product
from apps.user.models import Customer


class Order(models.Model):
    STATUS_CHOICES = [
        ("cancelled", "Cancelled"),
        ("complete", "Complete"),
        ("processing", "Processing"),
    ]

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    order_number = models.CharField(
        max_length=32, null=False, unique=True, editable=False
    )
    email = models.EmailField(max_length=254, null=False, blank=False)

    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label="(select country)", null=False, blank=False
    )
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_city = models.CharField(max_length=40, null=False, blank=False)
    address_line_1 = models.CharField(max_length=80, null=False, blank=False)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    shipping_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="processing"
    )
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _generate_order_number(self):
        """
        Generate a unique order number in the format
        {yymmdd}{hhmmss}{UUID(4CHARACTER)}.
        """
        date_part = now().strftime("%y%m%d%H%M%S")
        uuid_part = uuid.uuid4().hex[:4].upper()
        return f"{date_part}{uuid_part}"

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum("lineitem_total"))[
            "lineitem_total__sum"
        ] or Decimal("0.00")
        # Calculate shipping costs
        if self.order_total < config.FREE_DELIVERY_THRESHOLD:
            self.shipping_cost = self.lineitems.count() * Decimal(
                config.STANDARD_DELIVERY_PER_ITEM
            )
        else:
            self.shipping_cost = Decimal("0.00")

        self.grand_total = self.order_total + self.shipping_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "mood_order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False,
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total,
        and adjust the product stock without allowing it to go negative.
        """
        self.lineitem_total = self.product.price * self.quantity

        if not self.pk:
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save(update_fields=["stock"])
            else:
                raise ValueError(
                    f"Insufficient stock for product {self.product.name}"
                )

        super().save(*args, **kwargs)

        self.order.update_total()

    def delete(self, *args, **kwargs):
        """
        Override the original delete method to update the product stock and
        order total.
        """
        self.product.stock += self.quantity
        self.product.save(update_fields=["stock"])

        super().delete(*args, **kwargs)

        self.order.update_total()

    class Meta:
        db_table = "mood_order_item"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"SKU {self.product.sku} on order {self.order.order_number}"
