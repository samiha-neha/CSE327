from django.db import models
from django.contrib.auth.models import User
from cart.models import Product  


class Review(models.Model):
    """
    Model representing a product review submitted by a user.

    Attributes
    ----------
    user : User
        The user who submitted the review.
    product : Product
        The product being reviewed.
    rating : int
        Star rating given by the user (typically 1 to 5).
    comment : str
        Textual content of the review.
    created_at : datetime
        Timestamp when the review was created.
    updated_at : datetime
        Timestamp when the review was last updated.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        """
        Return a human-readable string representation of the review.

        :return: A string with the username and product name.
        :rtype: str
        """
        return f'Review by {self.user.username} on {self.product.name}'