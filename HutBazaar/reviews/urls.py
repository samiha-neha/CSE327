from django.urls import path
from . import views

app_name = 'review'

#: URL patterns for the review app.
urlpatterns = [
    path(
        'product/<int:product_id>/',
        views.product_reviews,
        name='product_reviews'
    ),
    path(
        'add/<int:product_id>/',
        views.add_review,
        name='add_review'
    ),
    path(
        'edit/<int:review_id>/',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'delete/<int:review_id>/',
        views.delete_review,
        name='delete_review'
    ),
]