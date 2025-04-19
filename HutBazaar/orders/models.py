# orders/models.py
import uuid
import datetime # Import datetime
from django.db import models
from django.utils import timezone # Import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe # Import mark_safe for image_preview

# --- Product Model ---
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
        """Provides an HTML preview of the image for the admin interface."""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="auto" />')
        return "(No image)"
    image_preview.short_description = 'Image Preview'


# --- Order Model ---
class Order(models.Model):
    # Inner Class for Order Status Choices
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    # Fields
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True, help_text="Unique identifier for tracking the order.")
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    # Use default=timezone.now to allow setting specific dates in tests and admin
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    # Default makes sense for an order total before items are added
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True) # Automatically updated on save
    estimated_delivery_date = models.DateField(blank=True, null=True, help_text="Estimated date the order will be delivered.")
    delivery_notes = models.TextField(blank=True, null=True, help_text="Notes regarding delivery, like tracking links or delay reasons.")

    # Meta Class for ordering
    class Meta:
        ordering = ['-order_date'] # Show newest orders first by default

    # Methods
    def __str__(self):
        """String representation of the Order model."""
        return f"Order {self.id} ({self.tracking_id})"

    def was_ordered_recently(self):
        """
        Returns True if the order was placed within the last day.
        """
        now = timezone.now()
        # Ensure order_date is not None before comparing
        if self.order_date is None:
             return False
        # Check if the order_date is within the range: (now - 1 day) <= order_date <= now
        return now - datetime.timedelta(days=1) <= self.order_date <= now
    # Attributes for better display in Django Admin
    was_ordered_recently.admin_order_field = 'order_date'
    was_ordered_recently.boolean = True
    was_ordered_recently.short_description = 'Ordered recently?'


# --- OrderItem Model ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Use PROTECT to prevent deleting a Product if it's part of an existing order
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product at the time the order was placed.") # Price at the time of order

    def __str__(self):
        """String representation of the OrderItem model."""
        # Use self.product.name if product relationship is guaranteed (which it should be)
        product_name = self.product.name if self.product else "Unknown Product"
        return f"{self.quantity} x {product_name} in Order {self.order.id}"

    def get_cost(self):
        """Calculates the total cost for this line item."""
        return self.price * self.quantity

    class Meta:
        # Optional: Ensure a product isn't added twice to the same order,
        # though often you might allow this and sum quantities later.
        # unique_together = ('order', 'product')
        pass