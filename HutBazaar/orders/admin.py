# orders/admin.py
from django.contrib import admin, messages
from .models import Product, Order, OrderItem

# Allows adding/editing OrderItems directly within the Order page
class OrderItemInline(admin.TabularInline): # Use StackedInline for vertical layout
    model = OrderItem
    extra = 0 # Don't show extra blank forms by default
    readonly_fields = ('price',) # Price is set at time of order, not editable here
    # You could add fields like 'product', 'quantity' if you want to build orders in admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns to display in the product list view
    list_display = ('name', 'price', 'stock', 'available', 'updated_at', 'image_preview')
    # Fields you can filter by on the right side
    list_filter = ('available', 'created_at', 'updated_at')
    # Fields you can search by
    search_fields = ('name', 'description')
    # Allow editing these fields directly in the list view (use with caution)
    list_editable = ('price', 'stock', 'available')
    # Fields that cannot be edited in the form (like calculated/auto fields)
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    # Customize the layout of the Add/Edit product form
    fieldsets = (
        (None, { # Section title (None means no title)
            'fields': ('name', 'description', 'price')
        }),
        ('Inventory & Status', {
            'fields': ('stock', 'available')
        }),
        ('Image', {
            'fields': ('image', 'image_preview') # Show upload field and preview
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Make this section initially hidden
        }),
    )
    # Django admin handles most basic validation errors automatically.
    # If you save a product with invalid data (e.g., non-numeric price),
    # Django will show an error message on the form. This fulfills the
    # "Admins see an error message if there is an issue updating" requirement
    # for standard validation. More complex errors would need custom code.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracking_id', 'customer_name', 'status', 'order_date', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'customer_email', 'tracking_id__iexact') # Allow searching by UUID
    # Make these fields read-only in the admin form
    readonly_fields = ('tracking_id', 'order_date', 'updated_at', 'total_amount')
    list_editable = ('status',) # Allow changing status from the list view
    date_hierarchy = 'order_date' # Adds handy date drill-down navigation
    inlines = [OrderItemInline] # Embed OrderItems within the Order page
    actions = ['mark_as_shipped'] # Add custom actions

    # Custom action definition
    def mark_as_shipped(self, request, queryset):
        updated_count = queryset.update(status=Order.OrderStatus.SHIPPED)
        self.message_user(request, f"{updated_count} orders marked as Shipped.", level=messages.SUCCESS)
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    # Override save_model to show the specific success message when ADDING an order via admin
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change) # Actually save the object
        if not change: # 'change' is False when adding a new object
            # Fulfills: "Admins will see the 'Order Listed Successfully' pop-up..."
            # Note: This message appears ONLY when an admin *creates* an order here.
            # It won't show when a customer places an order on the website.
            self.message_user(request, f"Order {obj.id} listed successfully.", level=messages.SUCCESS)
        # else: # Optional: message when editing an order
            # self.message_user(request, f"Order {obj.id} updated.", level=messages.SUCCESS)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # Basic display for OrderItems if accessed directly (usually managed via OrderAdmin)
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__tracking_id__iexact')
    readonly_fields = ('price',)