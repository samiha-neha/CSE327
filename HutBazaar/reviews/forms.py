from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for submitting and editing product reviews.

    Fields
    ------
    rating : int
        Star rating for the product (1 to 5).
    comment : str
        Optional comment about the product.
    """

    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Rating'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Comment',
        required=False
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']