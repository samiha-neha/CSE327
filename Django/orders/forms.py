# orders/forms.py
from django import forms

class OrderTrackingForm(forms.Form):
    tracking_id = forms.CharField(
        label="Your Tracking ID",
        max_length=40, # UUIDs are 36 chars + dashes
        widget=forms.TextInput(attrs={'placeholder': 'Enter your order tracking ID (e.g., 123e4567-e89b-12d3-a456-426614174000)'})
    )
