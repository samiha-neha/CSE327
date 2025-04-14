"""
URL configuration for the HutBazaar project.

This file defines the URL routes for the entire project. Routes are
delegated to individual apps such as cart and reviews.

For more information, see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from cart import views  # Import the views from the cart app


#: Project-level URL patterns.
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page URL
    path('cart/', include('cart.urls')),  # Cart app URLs
    path('reviews/', include('reviews.urls')),  # Reviews app URLs
    path('', views.index, name='index'),  # Root URL maps to cart.views.index
]