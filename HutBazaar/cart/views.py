"""
Cart views for e-commerce application.

Includes all cart-related operations such as adding items, removing items,
updating quantities, and rendering cart summaries. Each view is secured 
with user authentication and includes validation and user feedback.

References:
    Django messages framework: https://docs.djangoproject.com/en/stable/ref/contrib/messages/
    Django authentication decorators: https://docs.djangoproject.com/en/stable/topics/auth/default/#the-login-required-decorator
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import Cart, CartItem
from store.models import Product


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart with inventory validation.

    Args:
        request (HttpRequest): The request object.
        product_id (int): ID of the product to add.

    Returns:
        HttpResponseRedirect: Redirects to the cart view.
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

    return redirect('cart:view_cart')


@login_required
def view_cart(request):
    """
    Display the contents of the user's shopping cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered cart page.
    """
    cart = get_object_or_404(Cart, user=request.user)
    context = {'cart': cart}
    return render(request, 'cart/view_cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the shopping cart.

    Args:
        request (HttpRequest): The request object.
        item_id (int): ID of the cart item to remove.

    Returns:
        HttpResponseRedirect: Redirects to the cart view.
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

    Args:
        request (HttpRequest): The request object.
        item_id (int): ID of the cart item to update.

    Returns:
        HttpResponseRedirect: Redirects to the cart view.
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


@login_required
def cart_summary(request):
    """
    Return minimal cart data for AJAX requests (e.g., cart icon update).

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: Contains total item count and subtotal.
    """
    cart = get_object_or_404(Cart, user=request.user)
    return JsonResponse({
        'item_count': cart.total_items,
        'subtotal': cart.subtotal
    })






    