from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models.product import Product
from .models.category import Category


def home(request):
    """
    View for the home page, displaying products and categories.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    products = None
    category = Category.get_all_categories()

    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_product_by_category_id(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['product'] = products
    data['category'] = category
    return render(request, 'home.html', data)


def productdetail(request, pk):
    """
    View for displaying details of a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the product.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    product = Product.objects.get(pk=pk)
    return render(request, 'productdetail.html', {'product': product})