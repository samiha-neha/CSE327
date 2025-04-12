from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models.product import Product
from .models.category import Category




def home(request):
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


def productdetail(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'productdetail.html',{'product': product})