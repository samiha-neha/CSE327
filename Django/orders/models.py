# orders/models.py
import uuid
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # Import timezone

# --- Product Model remains the same ---
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, help_text="Number of items currently in stock")
    available = models.BooleanField(default=True, help_text="Is the product available for purchase?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="auto" />')
        return "(No image)"
    image_preview.short_description = 'Image Preview'


# --- Updated Order Model ---
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    # --- New Fields ---
    estimated_delivery_date = models.DateField(
        blank=True, null=True,
        help_text="Estimated date the order will be delivered."
    )
    delivery_notes = models.TextField(
        blank=True, null=True,
        help_text="Notes regarding delivery, like tracking links or delay reasons."
    )
    # --- End New Fields ---

    def __str__(self):
        return f"Order {self.id} ({self.tracking_id})"

    class Meta:
        ordering = ['-order_date']

# --- OrderItem Model remains the same ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity