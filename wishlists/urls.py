# wishlists/urls.py
from django.urls import path
from . import views

app_name = 'wishlists'

urlpatterns = [
    # Note: Included with /wishlist/ prefix in main urls.py
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-to-cart/<int:product_id>/', views.move_wishlist_item_to_cart, name='move_wishlist_item_to_cart'),
]