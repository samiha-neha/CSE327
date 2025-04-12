# orders/models.py
import uuid
import datetime # Import datetime
from django.db import models
from django.utils import timezone # Import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe # Needed for Product.image_preview

# --- Product Model (Seems okay, but added mark_safe import) ---
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
            # Ensure mark_safe is imported: from django.utils.safestring import mark_safe
            return mark_safe(f'<img src="{self.image.url}" width="100" height="auto" />')
        return "(No image)"
    image_preview.short_description = 'Image Preview'


# ---  Order Model (Corrected Indentation) ---
class Order(models.Model):
    # --- Inner Class: OrderStatus (Correctly Indented) ---
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')

    # --- Fields (Correctly Indented) ---
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    # Changed default=timezone.now TO auto_now_add=True based on original user code structure
    # auto_now_add=True means it's set only on creation. If you need to modify it later, remove auto_now_add.
    # If you need the field to be modifiable in tests like you were doing, USE default=timezone.now instead.
    # Let's revert to default=timezone.now to support the tests where you set the date explicitly.
    # order_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(default=timezone.now) # Use default to allow setting in tests
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery_date = models.DateField(blank=True, null=True, help_text="Estimated date the order will be delivered.")
    delivery_notes = models.TextField(blank=True, null=True, help_text="Notes regarding delivery, like tracking links or delay reasons.")
    # --- End Fields ---

    # --- Method: __str__ (Correctly Indented) ---
    def __str__(self):
        return f"Order {self.id} ({self.tracking_id})"

    # --- Method: was_ordered_recently (Correctly Indented) ---
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
    # --- End Method ---

    # --- Inner Class: Meta (Correctly Indented) ---
    class Meta:
        ordering = ['-order_date']
# --- End Order Model ---


# --- OrderItem Model (Seems okay) ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT) # PROTECT prevents deleting a Product if it's in an order
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity