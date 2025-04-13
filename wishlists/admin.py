# wishlists/admin.py
from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_count', 'created_at')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('products',) # Better widget for ManyToMany

    def get_item_count(self, obj):
        return obj.products.count()
    get_item_count.short_description = 'Number of Items'