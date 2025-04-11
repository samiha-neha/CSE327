from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('view/', views.view_cart, name='view_cart'),  # View the shopping cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add a product to the cart
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove an item from the cart
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),  # Update quantity of an item
    path('save_for_later/<int:item_id>/', views.save_for_later, name='save_for_later'),  # Save item for later purchase
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),  # Apply discount coupon
    path('estimate_shipping/', views.estimate_shipping, name='estimate_shipping'),  # Estimate shipping cost
]