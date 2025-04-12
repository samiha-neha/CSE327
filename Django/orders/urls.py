# orders/urls.py
from django.urls import path
from . import views # We will create views in the next step

app_name = 'orders' # This creates a namespace for URLs (e.g., 'orders:order_tracking')

urlpatterns = [
    # URL for the order tracking page: /orders/track/
    path('track/', views.order_tracking_view, name='order_tracking'),
    # Add other URLs specific to the orders app here later
    # Example: path('place/', views.place_order_view, name='place_order'),
]