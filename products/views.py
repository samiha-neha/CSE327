# products/views.py
from django.shortcuts import render
from .models import Product

def product_list_view(request):
    products = Product.objects.all().order_by('name')
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

# # Optional: Product Detail View
# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     context = {'product': product}
#     return render(request, 'products/product_detail.html', context)