from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
        
    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


    def __str__(self):
        return self.name

    

    