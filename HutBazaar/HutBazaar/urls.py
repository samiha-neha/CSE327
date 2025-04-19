# myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from django.conf import settings           # Import settings
from django.conf.urls.static import static # Import static helper
from orders.views import home_view 

admin.site.site_header = "Hut Bazaar Admin"
admin.site.site_title = "Hut Bazaar Portal" # Text in the browser <title> tag
admin.site.index_title = "Welcome to the Admin Area" # Text on the admin index page

urlpatterns = [
    path('admin/', admin.site.urls), # URL for the admin panel
    path('', home_view, name='home'), 
    # Any URL starting with 'orders/' will be handled by the orders app's urls.py
    path('orders/', include('orders.urls', namespace='orders')),
    # Add other project-wide URLs here if needed
    # Example: path('', include('homepage.urls')),
]

# IMPORTANT: Add this for serving media files (like product images) during DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)