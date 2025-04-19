from django.db import models
from django.conf import settings
from store.models import Product


class Review(models.Model):
    """
    Model representing a product review.

    Attributes:
        product (ForeignKey): The product being reviewed.
        user (ForeignKey): The user who created the review.
        rating (PositiveIntegerField): Rating from 1 to 5.
        comment (TextField): The review text content.
        created_at (DateTimeField): When the review was created.
        updated_at (DateTimeField): When the review was last updated.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        """String representation of the review."""
        return f"Review by {self.user.username} for {self.product.name}"

    @property
    def stars(self):
        """Return rating as a string of stars."""
        return '★' * self.rating + '☆' * (5 - self.rating)
        