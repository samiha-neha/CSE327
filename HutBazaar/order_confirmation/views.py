from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from checkout.models import Order
from .models import OrderConfirmation
import pdfkit


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Create or get confirmation record
    confirmation, created = OrderConfirmation.objects.get_or_create(order=order)

    if created or not confirmation.email_sent:
        send_confirmation_email(order)
        confirmation.email_sent = True
        confirmation.save()

    context = {"order": order, "confirmation": confirmation}
    return render(request, "order_confirmation/confirmation.html", context)


def send_confirmation_email(order):
    subject = f"Order Confirmation #{order.id}"
    message = render_to_string(
        "order_confirmation/email_confirmation.txt", {"order": order}
    )
    html_message = render_to_string(
        "order_confirmation/email_confirmation.html", {"order": order}
    )

    recipient = order.user.email if order.user else None
    if recipient:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            html_message=html_message,
        )


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def download_receipt(request, order_id):
    try:
        # Get the order
        order = get_object_or_404(Order, id=order_id)

        # Get cart items from session
        cart_items = request.session.get(f"order_{order.id}_items", [])
        if not cart_items:
            cart_items = [
                {"name": "Unknown Item", "price": order.total, "quantity": 1}
            ]  # Fallback

        # Create the PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="receipt_{order.id}.pdf"'
        )

        # Create the PDF object
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Header
        p.setFont("Helvetica-Bold", 16)
        p.drawString(1 * inch, height - 1 * inch, f"Receipt #{order.id}")

        # Order details
        p.setFont("Helvetica", 12)
        p.drawString(
            1 * inch,
            height - 1.5 * inch,
            f"Date: {order.created_at.strftime('%Y-%m-%d')}",
        )
        p.drawString(1 * inch, height - 1.75 * inch, f"Email: {order.email}")
        p.drawString(
            1 * inch, height - 2 * inch, f"Payment Method: {order.payment_method}"
        )

        # Shipping address
        p.drawString(1 * inch, height - 2.5 * inch, "Shipping Address:")
        p.drawString(1 * inch, height - 2.75 * inch, f"{order.shipping_address}")
        p.drawString(
            1 * inch,
            height - 3 * inch,
            f"{order.shipping_city}, {order.shipping_state} {order.shipping_zip}",
        )

        # Items header
        p.setFont("Helvetica-Bold", 12)
        p.drawString(1 * inch, height - 3.5 * inch, "Items Purchased:")

        # List items with price and quantity
        y_position = height - 3.75 * inch
        p.setFont("Helvetica", 12)
        for item in cart_items:
            line = f"{item['quantity']}x {item['name']} - ${item['price']} each"
            p.drawString(1 * inch, y_position, line)
            y_position -= 0.25 * inch  # Move down for next item
            if y_position < 1 * inch:  # Basic page overflow check
                p.showPage()
                y_position = height - 1 * inch
                p.setFont("Helvetica", 12)

        # Total
        p.setFont("Helvetica-Bold", 14)
        p.drawString(1 * inch, y_position - 0.5 * inch, f"Total: ${order.total}")

        # Finalize the PDF
        p.showPage()
        p.save()

        # Clean up session (optional)
        if f"order_{order.id}_items" in request.session:
            del request.session[f"order_{order.id}_items"]

        return response
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)
