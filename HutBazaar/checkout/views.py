from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import Order  # Assuming you have an Order model
from .forms import CheckoutForm  # Assuming you have this


def checkout_view(request):
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
            )

            # Store cart items in session for receipt
            request.session[f"order_{order.id}_items"] = cart.items

            if (
                settings.DEBUG
            ):  # Only send email if in debug mode (as per your original logic)
                try:
                    send_mail(
                        f"Order #{order.id} Confirmation",
                        f"Thank you for your order #{order.id}. Total: ${order.total}",
                        settings.DEFAULT_FROM_EMAIL,
                        [form.cleaned_data["email"]],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Email not sent: {e}")  # Print error to console but continue

            return redirect("order_confirmation:confirmation", order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["email"] = request.user.email
        form = CheckoutForm(initial=initial)

    return render(request, "checkout.html", {"form": form, "cart": cart})
