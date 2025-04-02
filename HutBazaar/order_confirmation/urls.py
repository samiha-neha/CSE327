from django.urls import path
from . import views

app_name = "order_confirmation"

urlpatterns = [
    path("<int:order_id>/", views.order_confirmation, name="confirmation"),
    path("<int:order_id>/receipt/", views.download_receipt, name="download_receipt"),
]
