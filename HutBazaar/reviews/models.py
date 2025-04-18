from django.db import models
from django.contrib.auth.models import User
from cart.models import Product  


class Review(models.Model):
    """Represents a product review submitted by a user.

    Attributes:
        user (User): The reviewer.
        product (Product): Reviewed product.
        rating (int): Star rating (1-5).
        comment (str): Review text content.
        created_at (datetime): When review was created.
        updated_at (datetime): When review was last updated.
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