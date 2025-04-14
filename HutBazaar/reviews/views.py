from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET

from .models import Review
from cart.models import Product, OrderItem
from .forms import ReviewForm


@require_GET
def product_reviews(request, product_id):
    """
    Display product reviews.

    :param request: HttpRequest object.
    :param product_id: ID of the product.
    :return: Rendered HTML page with product reviews.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')
    verified_buyer = False

    if request.user.is_authenticated:
        verified_buyer = OrderItem.objects.filter(
            product=product, order__user=request.user
        ).exists()

    return render(
        request,
        'review/product_reviews.html',
        {
            'product': product,
            'reviews': reviews,
            'verified_buyer': verified_buyer
        }
    )


@login_required
def add_review(request, product_id):
    """
    Add a review for a product.

    :param request: HttpRequest object.
    :param product_id: ID of the product to review.
    :return: Redirect or rendered HTML page to add review.
    """
    product = get_object_or_404(Product, id=product_id)
    has_purchased = OrderItem.objects.filter(
        product=product, order__user=request.user
    ).exists()

    if not has_purchased:
        messages.error(request, "You can only review products you have purchased.")
        return redirect('review:product_reviews', product_id=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            messages.success(request, "Your review has been submitted.")
            return redirect('review:product_reviews', product_id=product.id)
    else:
        form = ReviewForm()

    return render(
        request,
        'review/add_review.html',
        {'form': form, 'product': product}
    )


@login_required
def edit_review(request, review_id):
    """
    Edit an existing review.

    :param request: HttpRequest object.
    :param review_id: ID of the review to edit.
    :return: Redirect or rendered HTML page to edit review.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect('review:product_reviews', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        'review/edit_review.html',
        {'form': form, 'review': review}
    )


@login_required
def delete_review(request, review_id):
    """
    Delete an existing review.

    :param request: HttpRequest object.
    :param review_id: ID of the review to delete.
    :return: Redirect or rendered confirmation page.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, "Review deleted.")
        return redirect('review:product_reviews', product_id=product_id)

    return render(
        request,
        'review/confirm_delete.html',
        {'review': review}
    )