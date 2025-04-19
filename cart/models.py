from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from store.models.product import Product


class Cart(models.Model):
    """Model representing a user's shopping cart.

    Attributes:
        user (User): The user who owns the cart.
        created_at (datetime): Timestamp of when the cart was created.
        updated_at (datetime): Timestamp of the last update.
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
        """Return string representation of the cart."""
        return f"Cart #{self.id} for {self.user.username}"

    @property
    def total_items(self):
        """Return total quantity of items in cart.

        :return: Sum of quantities of all cart items.
        :rtype: int
        """
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate subtotal before any discounts or taxes.

        :return: Subtotal cost of all items.
        :rtype: float
        """
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Model representing an item in a shopping cart.

    Attributes:
        cart (Cart): The cart that contains this item.
        product (Product): The product added to the cart.
        quantity (int): The quantity of the product.
        added_at (datetime): When the item was added to the cart.
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
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')

    def __str__(self):
        """Return string representation of the cart item."""
        return f"{self.quantity}x {self.product.name} in cart #{self.cart.id}"

    @property
    def total_price(self):
        """Calculate total price for this line item.

        :return: Price * quantity.
        :rtype: float
        """
        return self.product.price * self.quantity

    def clean(self):
        """Validate the cart item before saving.

        :raises ValidationError: If quantity is less than 1 or exceeds stock.
        """
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
    """Update cart's timestamp when items change.

    :param sender: The model class.
    :param instance: The instance of CartItem being saved or deleted.
    """
    instance.cart.save()