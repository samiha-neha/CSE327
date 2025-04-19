from django.contrib import admin
from django.urls import path
from store import views

app_name = 'store'  

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),

]