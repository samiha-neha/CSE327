# orders/views.py
# This file remains the same as in the previous unified guide
from django.shortcuts import render, get_object_or_404
from .models import Order
from .forms import OrderTrackingForm
import uuid

def order_tracking_view(request):
    """Handles the order tracking page.

    Allows users to submit a tracking ID via a form (POST) or view the
    empty form (GET). If a valid tracking ID is submitted, it attempts
    to retrieve the corresponding Order object and displays its details.
    Handles invalid ID formats and non-existent orders by displaying
    error messages.

    :param request: The HttpRequest object containing form data if POST.
    :type request: django.http.HttpRequest
    :returns: Renders the 'orders/order_tracking.html' template with
              context containing the form, the found order (if any),
              and any error messages.
    :rtype: django.http.HttpResponse
    """
    order = None
    error_message = None
    form = OrderTrackingForm()

    if request.method == 'POST':
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            tracking_id_str = form.cleaned_data['tracking_id']
            try:
                tracking_uuid = uuid.UUID(tracking_id_str, version=4)
                # This retrieves the order, including the new fields
                order = get_object_or_404(Order, tracking_id=tracking_uuid)
            except ValueError:
                # Handles "error message if order details cannot be retrieved" (invalid format)
                error_message = "Invalid tracking ID format. Please check and try again."
            except Order.DoesNotExist:
                 # Handles "error message if order details cannot be retrieved" (not found)
                error_message = "Order not found. Please verify your tracking ID."
            except Exception as e:
                print(f"Error looking up tracking ID {tracking_id_str}: {e}")
                # Handles "error message if order details cannot be retrieved" (other errors)
                error_message = "An unexpected error occurred. Please try again later."

    context = {
        'form': form,
        'order': order,
        'error_message': error_message,
    }
    return render(request, 'orders/order_tracking.html', context)