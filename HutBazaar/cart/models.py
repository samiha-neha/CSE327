"""
Cart application models with automatic total calculation via signals.

Includes:
- Cart: Represents a user's shopping cart
- CartItem: Individual products in the cart
- OrderItem: Completed/purchased items (converted from CartItem)
"""

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from store.models.product import Product 
from django.core.exceptions import ValidationError

class Cart(models.Model):
    """
    Represents a user's shopping cart.

    Attributes:
        user (OneToOneField): Reference to the user who owns this cart.
        created_at (DateTime): When the cart was created.
        updated_at (DateTime): When the cart was last modified.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"

    @property
    def total_items(self):
        """Return total quantity of items in cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate subtotal before any discounts or taxes."""
        return sum(item.total_price for item in self.items.all())

    def convert_to_order(self, user):
        """Convert all cart items to order items."""
        order_items = [
            OrderItem(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                user=user,
                ordered=True
            )
            for item in self.items.all()
        ]
        OrderItem.objects.bulk_create(order_items)
        self.items.all().delete()
        return order_items


class CartItem(models.Model):
    """
    Represents an individual product item in a shopping cart.

    Attributes:
        cart (ForeignKey): Parent cart.
        product (ForeignKey): Product being purchased.
        quantity (PositiveInteger): Number of units.
        saved_for_later (Boolean): If saved for later purchase.
        added_at (DateTime): When item was added to cart.
    """

    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    saved_for_later = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart #{self.cart.id}"

    @property
    def total_price(self):
        """Calculate total price for this line item."""
        return self.product.price * self.quantity

    def clean(self):
        """Validate the cart item before saving."""
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1")
        
        if hasattr(self.product, 'inventory'):
            if self.quantity > self.product.inventory.stock:
                raise ValidationError(
                    f"Only {self.product.inventory.stock} available in stock"
                )


class OrderItem(models.Model):
    """
    Represents a purchased item (converted from CartItem).

    Attributes:
        product (ForeignKey): Purchased product (protected from deletion)
        quantity (PositiveInteger): Number of units ordered
        price (Decimal): Price at time of purchase (snapshot)
        ordered (Boolean): Marks completed orders
        ordered_date (DateTime): When purchase was completed
        user (ForeignKey): User who made the purchase
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # Protect order history
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['-ordered_date']

    def __str__(self):
        status = "Ordered" if self.ordered else "Pending"
        return f"{self.quantity}x {self.product.name} ({status})"

    def save(self, *args, **kwargs):
        """Snapshot the product price when saving."""
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Calculate total price for this ordered item."""
        return self.price * self.quantity


# Signals
@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_timestamp(sender, instance, **kwargs):
    """Update cart's modified timestamp when items change."""
    instance.cart.save()