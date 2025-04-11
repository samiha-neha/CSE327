from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import Order  # Assuming you have an Order model
from .forms import CheckoutForm  # Assuming you have this
from .models import Discount


def checkout_view(request):
    """Handle the checkout process and create an order.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the checkout page or redirects after order creation.

    Notes:
        Uses a temporary mock cart until the real cart is integrated.
        Stores cart items in the session for receipt generation.
    """

    # Temporary cart mock - replace with real cart when available
    class Cart:
        def __init__(self):
            self.items = [
                {"name": "Sample Product 1", "price": 19.99, "quantity": 2},
                {"name": "Sample Product 2", "price": 29.99, "quantity": 1},
            ]
            self.total = sum(item["price"] * item["quantity"] for item in self.items)

        def is_empty(self):
            return len(self.items) == 0

    cart = Cart()

    if cart.is_empty():
        messages.warning(request, "Your cart is empty")
        return redirect("checkout:checkout")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data.get("coupon_code")
            discount = None

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
            # Process the order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=form.cleaned_data["email"],
                total=cart.total,
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
            request.session[f"order_{order.id}_items"] = cart.items

            return redirect("order_confirmation:confirmation", order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["email"] = request.user.email
        form = CheckoutForm(initial=initial)

    return render(request, "checkout.html", {"form": form, "cart": cart})
