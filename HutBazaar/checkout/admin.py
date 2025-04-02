from django.contrib import admin

# Register your models here.
from .models import Order, Discount

admin.site.register(Order)
admin.site.register(Discount)
