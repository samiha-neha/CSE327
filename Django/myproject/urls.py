# myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from django.conf import settings           # Import settings
from django.conf.urls.static import static # Import static helper

urlpatterns = [
    path('admin/', admin.site.urls), # URL for the admin panel
    # Any URL starting with 'orders/' will be handled by the orders app's urls.py
    path('orders/', include('orders.urls', namespace='orders')),
    # Add other project-wide URLs here if needed
    # Example: path('', include('homepage.urls')),
]

# IMPORTANT: Add this for serving media files (like product images) during DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)