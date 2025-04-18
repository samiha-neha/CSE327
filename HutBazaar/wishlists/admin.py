from django.contrib import admin
from .models import Wishlist, WishlistItem  # Import both models with correct capitalization

admin.site.register(Wishlist)
admin.site.register(WishlistItem) # Register WishlistItem if you want it in the admin