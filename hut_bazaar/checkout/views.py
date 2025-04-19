from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import Order
from .forms import CheckoutForm
from .models import Discount
from cart.models import Cart, CartItem


def checkout_view(request):
    """Handle the checkout process and create an order.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the checkout page or redirects after order creation.
        Returns form and cart information to show in html template

    Notes:
        Checks for Voucher verification
        Now uses the real cart from the cart app instead of mock data.
        Stores cart items in the session for receipt in the confirmation app.
    """

    # Temporary cart mock - replace with real cart when available
    # class Cart:
    #     def __init__(self):
    #         self.items = [
    #             {"name": "Sample Product 1", "price": 19.99, "quantity": 2},
    #             {"name": "Sample Product 2", "price": 29.99, "quantity": 1},
    #         ]
    #         self.total = sum(item["price"] * item["quantity"] for item in self.items)

    #     def is_empty(self):
    #         return len(self.items) == 0

    # cart = Cart()

    # Login check
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to proceed to checkout")
        return redirect("users:login")

    # Get the user cart from database
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty")
        return redirect("store:home")

    # Check if cart has items
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect("store:home")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data.get("coupon_code")
            discount = None

            # Voucher verification
            if coupon_code:
                try:
                    discount = Discount.objects.get(code=coupon_code)
                    if discount.is_used_by_user(request.user):
                        messages.error(request, "This voucher has already been used")
                        return redirect("checkout:checkout")
                    if not discount.is_valid_for_user(request.user):
                        messages.error(request, "This voucher is no longer valid")
                        return redirect("checkout:checkout")
                except Discount.DoesNotExist:
                    messages.error(request, "Invalid voucher code")
                    return redirect("checkout:checkout")

            # Process the order creation
            order = Order.objects.create(
                user=request.user,
                email=form.cleaned_data["email"],
                total=cart.subtotal,
                payment_method=form.cleaned_data["payment_method"],
                shipping_address=form.cleaned_data["shipping_address"],
                shipping_city=form.cleaned_data["shipping_city"],
                shipping_state=form.cleaned_data["shipping_state"],
                shipping_zip=form.cleaned_data["shipping_zip"],
                is_paid=False,
                payment_status="pending",
                discount_coupon_used=discount,
            )

            # Store cart items in session for receipt
            # Convert CartItems to a serializable format for session storage
            request.session[f"order_{order.id}_items"] = [
                {
                    "name": item.product.name,
                    "price": float(item.product.price),
                    "quantity": item.quantity,
                    "total_price": float(item.total_price),
                }
                for item in cart.items.all()
            ]

            # Clear the cart after successful order
            cart.items.all().delete()

            return redirect("order_confirmation:confirmation", order_id=order.id)
    else:
        # Pre-populate form with user's email if authenticated
        initial = {"email": request.user.email} if request.user.is_authenticated else {}
        form = CheckoutForm(initial=initial)

    # Prepare cart items data for template
    cart_items_for_template = [
        {
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "total_price": item.total_price,
        }
        for item in cart.items.all()
    ]

    context = {
        "form": form,
        "cart": {"items": cart_items_for_template, "total": cart.subtotal},
    }
    return render(request, "checkout/checkout.html", context)
