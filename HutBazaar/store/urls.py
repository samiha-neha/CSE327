from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('', views.home),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),

]