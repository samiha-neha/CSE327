from django import forms
from .models import OrderConfirmation


class OrderConfirmationForm(forms.ModelForm):
    class Meta:
        model = OrderConfirmation
        fields = []  # No fields needed for basic confirmation
