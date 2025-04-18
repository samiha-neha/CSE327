"""
URL configuration for the HutBazaar project.

This file defines the URL routes for the entire project. 
Routes are specific to individual apps such as cart and reviews.

"""

from django.contrib import admin
from django.urls import path, include
from cart import views  # Import the views from the cart app

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),  # Cart-specific URLs
    path('reviews/', include('reviews.urls')),
    path("", include("store.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

