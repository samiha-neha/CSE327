# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Note: Included with /products/ prefix in main urls.py
    path('', views.product_list_view, name='product_list'),
    # Optional: path('<int:product_id>/', views.product_detail_view, name='product_detail'),
]