# wishlists/models.py
from django.db import models
from django.conf import settings
from products.models import Product # Import Product from the other app

class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist' # Access via user.wishlist
    )
    products = models.ManyToManyField(
        Product, # Link to Product model
        blank=True,
        related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"