"""
Context processors for cart application.
"""

from .models import Cart


def cart_items(request):
    """
    Add cart item count to template context for all pages.

    Args:
        request: HttpRequest object.

    Returns:
        dict: Context with cart item count if user is authenticated.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        return {
            'cart_item_count': cart.total_items if cart else 0,
            'cart_subtotal': cart.subtotal if cart else 0
        }
    return {'cart_item_count': 0, 'cart_subtotal': 0}