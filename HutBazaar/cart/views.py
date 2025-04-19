from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import Cart, CartItem
from store.models import Product
from django.core.cache import cache


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart or update quantity if it already exists.

    :param request: The HTTP request object.
    :param product_id: ID of the product to be added.
    :return: Redirects to the previous page or store home.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    try:
        item = CartItem.objects.filter(cart=cart, product=product).first()

        if item:
            item.quantity += 1
            item.full_clean()
            item.save()
            messages.success(request, "Item quantity updated in cart.")
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=1)
            messages.success(request, "Item added to cart.")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


@login_required
def view_cart(request):
    """
    Display the contents of the user's shopping cart.

    :param request: The HTTP request object.
    :return: Rendered cart page with cart items.
    """
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the shopping cart.

    :param request: The HTTP request object.
    :param item_id: ID of the cart item to be removed.
    :return: Redirects to the cart view.
    """
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f"Removed {product_name} from cart.")
    return redirect('cart:view_cart')


@login_required
def update_quantity(request, item_id):
    """
    Update the quantity of an item in the cart.

    :param request: The HTTP request object.
    :param item_id: ID of the cart item to update.
    :return: Redirects to the cart view.
    """
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError("Quantity must be at least 1")

        item.quantity = new_quantity
        item.full_clean()
        item.save()
        messages.success(request, "Quantity updated.")
    except (ValueError, ValidationError) as e:
        messages.error(request, str(e))

    return redirect('cart:view_cart')


def cart_summary(request):
    """
    Get cart summary data for display in templates.

    :param request: The HTTP request object.
    :return: A dictionary with item count and subtotal.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {
                'item_count': cart.total_items,
                'subtotal': cart.subtotal
            }
    return {'item_count': 0, 'subtotal': 0}