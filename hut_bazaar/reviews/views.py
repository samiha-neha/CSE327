from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from store.models import Product

@login_required
def add_review(request, product_id):
    """
    Handle adding a new review for a product.

    Args:
        request (HttpRequest): The request object.
        product_id (int): ID of the product being reviewed.

    Returns:
        HttpResponseRedirect: Redirects to product detail page.
    """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating:
            messages.error(request, "Please select a rating")
            return redirect('store:product-detail', pk=product_id) 

        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        messages.success(request, "Your review has been saved")
        return redirect('store:product-detail', pk=product_id) 

    return redirect('store:product-detail', pk=product_id) 


@login_required
def delete_review(request, review_id):
    """
    Handle deleting a review.
    
    Args:
        request (HttpRequest): The request object
        review_id (int): ID of the review to delete
        
    Returns:
        HttpResponseRedirect: Redirects to product detail page
    """
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, "Your review has been deleted")
    return redirect('store:product-detail', pk=product_id) 


def product_reviews(request, product_id):
    """
    Display all reviews for a specific product.

    Args:
        request (HttpRequest): The request object.
        product_id (int): ID of the product.

    Returns:
        HttpResponse: Rendered reviews page.
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'reviews/product_reviews.html', {
        'product': product,
        'reviews': reviews
    })