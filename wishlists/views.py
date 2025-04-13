# wishlists/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product # Import Product
from .models import Wishlist

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all().order_by('name') # Get products from wishlist
    context = {
        'wishlist': wishlist,
        'products': products,
    }
    return render(request, 'wishlists/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f"'{product.name}' added to wishlist.")
    else:
        messages.info(request, f"'{product.name}' is already in wishlist.")

    # Redirect back to where user came from, or wishlist as fallback
    return redirect(request.META.get('HTTP_REFERER', 'wishlists:wishlist'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Ensure wishlist exists for the user before trying to remove
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f"'{product.name}' removed from wishlist.")
    else:
        messages.info(request, f"'{product.name}' was not in wishlist.")

    return redirect('wishlists:wishlist') # Always redirect to wishlist page after removal


# --- Placeholder for moving to cart ---
# You would need a separate 'cart' app/logic for this to actually work
@login_required
def move_wishlist_item_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    # --- Add to Cart Logic (REPLACE WITH YOUR CART IMPLEMENTATION) ---
    # cart = Cart(request) # Example: Get cart from session
    # cart.add(product=product, quantity=1)
    messages.info(request, f"'{product.name}' -> Add to Cart (Not Implemented)") # Placeholder
    # --- End Cart Logic ---

    # Remove from wishlist after adding to cart
    wishlist.products.remove(product)

    # Redirect to cart page or wishlist page
    # return redirect('cart:detail')
    return redirect('wishlists:wishlist')