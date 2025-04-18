
from django.db import models
from .category import Category


class Product(models.Model):
    """
    Model representing a product.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1
    )
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        """
        Returns the name of the product as a string.
        """
        return self.name

    @staticmethod
    def get_all_products():
        """
        Retrieves all products from the database.

        Returns:
            QuerySet: A QuerySet containing all Product objects.
        """
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        """
        Retrieves products filtered by category ID.  If no category_id
        is provided, returns all products.

        Args:
            category_id (int): The ID of the category to filter by.

        Returns:
            QuerySet: A QuerySet containing the filtered Product objects,
                      or all Product objects if category_id is None.
        """
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
    