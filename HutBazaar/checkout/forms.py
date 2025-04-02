from django import forms


class CheckoutForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "your@email.com"})
    )
    shipping_address = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Enter your full shipping address"}
        )
    )
    shipping_city = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "City"})
    )
    shipping_state = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "State/Province"})
    )
    shipping_zip = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "ZIP/Postal Code"})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("credit_card", "Credit Card"),
            ("paypal", "PayPal"),
            ("bank_transfer", "Bank Transfer"),
        ],
        widget=forms.RadioSelect,
    )
    coupon_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter coupon code (optional)"}),
    )
