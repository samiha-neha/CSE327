from django.db import models

# Create your models here.
"""
Cart app models with mock product references.
"""
from django.conf import settings


class Cart(models.Model):
    """
    Shopping cart model associated with a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"


class CartItem(models.Model):
    """
    Represents an individual item in the cart.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    saved_for_later = models.BooleanField(default=False)

    @property
    def total_price(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class CartItem(models.Model):
    """
    Model for a single item in the user's shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    saved_for_later = models.BooleanField(default=False)

    def total_price(self):
        """
        Calculate the total price for the item based on quantity and product price.

        Returns:
            Decimal: Total price for this cart item.
        """
        return self.product_price * self.quantity