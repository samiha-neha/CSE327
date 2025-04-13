# myproject/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from django.conf import settings
from django.conf.urls.static import static
# Optional: Import a view for a basic homepage
# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs (we'll define the include targets later)
    path('products/', include('products.urls', namespace='products')),
    path('profile/', include('userprofiles.urls', namespace='userprofiles')),
    path('wishlist/', include('wishlists.urls', namespace='wishlists')),

    # Django Auth URLs
    path('accounts/', include('django.contrib.auth.urls')), # for login, logout, password reset etc.

    # Basic Homepage (Optional)
    # path('', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    path('', lambda request: redirect('products:product_list', permanent=False), name='homepage'), # Redirect homepage to product list for now
]

# Serve media files during development (if using ImageField)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)