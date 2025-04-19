from django.db import models


class Category(models.Model):
    """
    Model representing a category.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the name of the category as a string.
        """
        return self.name

    @staticmethod
    def get_all_categories():
        """
        Retrieves all categories from the database.

        Returns:
            QuerySet: A QuerySet containing all Category objects.
        """
        return Category.objects.all()
