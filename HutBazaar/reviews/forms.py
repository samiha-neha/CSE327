from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """
    Form for submitting or editing product reviews.
    """

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }