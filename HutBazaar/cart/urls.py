"""
URL configuration for cart application.
"""

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('', views.index, name='index'), 
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('summary/', views.cart_summary, name='cart_summary'),
]

