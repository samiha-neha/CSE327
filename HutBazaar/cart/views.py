from django.shortcuts import render

"""
Cart views for adding, removing, and updating items.
"""

from django.shortcuts import redirect
from .models import Cart, CartItem
from .mock_data import get_product_by_id


def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.
    """
    product = get_product_by_id(product_id)
    if not product:
        return render(request, 'cart/error.html', {"message": "Product not found."})

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_id=product["id"],
        defaults={
            "product_name": product["name"],
            "product_price": product["price"],
            "quantity": 1,
        },
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart:view_cart')


def view_cart(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # You can change 'login' to your actual login view name

    # Proceed with the cart logic if the user is authenticated
    cart = Cart.objects.filter(user=request.user).first()
    
    # Handle cases where no cart is found for the user
    if not cart:
        # Create an empty cart or handle it differently
        cart = None

    return render(request, 'cart/view_cart.html', {'cart': cart})


def remove_from_cart(request, item_id):
    """
    Remove an item from the user's cart.

    Args:
        request: The request object.
        item_id: The ID of the cart item to remove.
    """
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if item:
            item.delete()
    
    return redirect('cart:view_cart')


def update_quantity(request, item_id):
    """
    Update the quantity of an item in the user's cart.

    Args:
        request: The request object.
        item_id: The ID of the cart item to update.
    """
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if item:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()
    
    return redirect('cart:view_cart')


def save_for_later(request, item_id):
    """
    Save an item for later purchase in the user's cart.

    Args:
        request: The request object.
        item_id: The ID of the cart item to save for later.
    """
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if item:
            item.saved_for_later = True
            item.save()

    return redirect('cart:view_cart')


def apply_coupon(request):
    """
    Apply a discount coupon to the cart.

    Args:
        request: The request object.
    """
    coupon_code = request.POST.get('coupon_code')
    discount = 0

    if coupon_code == 'DISCOUNT10':
        discount = 10  # 10% discount

    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        total_price = sum([item.total_price() for item in cart.items.all()])
        discounted_price = total_price - (total_price * discount / 100)

    return render(request, 'cart/view_cart.html', {'cart': cart, 'discounted_price': discounted_price})


def estimate_shipping(request):
    """
    Estimate the shipping cost based on the user's location.

    Args:
        request: The request object.
    """
    shipping_cost = 0
    location = request.POST.get('location')

    if location == 'USA':
        shipping_cost = 5
    elif location == 'Europe':
        shipping_cost = 10
    else:
        shipping_cost = 15

    return render(request, 'cart/view_cart.html', {'shipping_cost': shipping_cost})


def index(request):
    return render(request, 'index.html')  # This will render the index.html template  
 





    