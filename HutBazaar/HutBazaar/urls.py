"""
URL configuration for the HutBazaar project.

This file defines the URL routes for the entire project.
Routes are specific to individual apps such as cart and reviews.

"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("reviews/", include("reviews.urls")),
    path("checkout/", include("checkout.urls")),
    path("order-confirm/", include("order_confirmation.urls")),
    path("users/", include("users.urls")),
    path("users/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("store.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
