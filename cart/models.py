"""
Cart application models with automatic total calculation via signals.
"""

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from store.models import Product


class Cart(models.Model):
    """
    Represents a user's shopping cart.

    Attributes:
        user (ForeignKey): Reference to the user who owns this cart.
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
        """String representation of the cart."""
        return f"Cart #{self.id} for {self.user.username}"

    @property
    def total_items(self):
        """Return total quantity of items in cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate subtotal before any discounts or taxes."""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """
    Represents an individual product item in a shopping cart.

    Attributes:
        cart (ForeignKey): Reference to the parent cart.
        product (ForeignKey): Reference to the product being purchased.
        quantity (PositiveInteger): Number of units in cart.
        saved_for_later (Boolean): If item is saved for later purchase.
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
        """String representation of cart item."""
        return f"{self.quantity}x {self.product.name} in cart #{self.cart.id}"

    @property
    def total_price(self):
        """Calculate total price for this line item."""
        return self.product.price * self.quantity

    def clean(self):
        """Validate the cart item before saving."""
        from django.core.exceptions import ValidationError
        
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1")
        
        if hasattr(self.product, 'inventory'):
            if self.quantity > self.product.inventory.stock:
                raise ValidationError(
                    f"Only {self.product.inventory.stock} available in stock"
                )


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_timestamp(sender, instance, **kwargs):
    """
    Signal receiver to update cart's timestamp when items change.

    Args:
        sender: The model class sending the signal.
        instance: The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    instance.cart.save()