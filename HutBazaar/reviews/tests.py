"""
Unit testing for the reviews app

These tests include
- Creating a review by a verified buyer
- Preventing non-buyers from submitting reviews
- Editing and deleting reviews
- Viewing product reviews

"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from cart.models import Product, OrderItem, Order
from reviews.models import Review

class ReviewTests(TestCase):
    """Test suite for the reviews app."""

    def setUp(self):
        """Set up initial test data."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', price=10.00, stock=5)

        self.order = Order.objects.create(user=self.user, is_ordered=True)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def test_verified_buyer_can_add_review(self):
        """Test that a verified buyer can submit a review."""
        self.client.login(username='testuser', password='password')
        response = self.client.post(
            reverse('review:add_review', args=[self.product.id]),
            {'rating': 5, 'comment': 'Excellent!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product).exists())

    def test_non_buyer_cannot_add_review(self):
        """Test that a user who hasn't purchased the product cannot submit a review."""
        new_user = User.objects.create_user(username='nonbuyer', password='password')
        self.client.login(username='nonbuyer', password='password')
        response = self.client.post(
            reverse('review:add_review', args=[self.product.id]),
            {'rating': 3, 'comment': 'Average'}
        )
        self.assertRedirects(response, reverse('review:product_reviews', args=[self.product.id]))
        self.assertFalse(Review.objects.filter(user=new_user, product=self.product).exists())

    def test_edit_review(self):
        """Test that a user can edit their review."""
        Review.objects.create(user=self.user, product=self.product, rating=4, comment='Good')
        self.client.login(username='testuser', password='password')
        review = Review.objects.get(user=self.user, product=self.product)
        response = self.client.post(
            reverse('review:edit_review', args=[review.id]),
            {'rating': 5, 'comment': 'Updated review'}
        )
        self.assertRedirects(response, reverse('review:product_reviews', args=[self.product.id]))
        review.refresh_from_db()
        self.assertEqual(review.comment, 'Updated review')

    def test_delete_review(self):
        """Test that a user can delete their review."""
        Review.objects.create(user=self.user, product=self.product, rating=4, comment='Nice')
        self.client.login(username='testuser', password='password')
        review = Review.objects.get(user=self.user, product=self.product)
        response = self.client.post(reverse('review:delete_review', args=[review.id]))
        self.assertRedirects(response, reverse('review:product_reviews', args=[self.product.id]))
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_view_product_reviews(self):
        """Test that anyone can view product reviews."""
        Review.objects.create(user=self.user, product=self.product, rating=4, comment='Good')
        response = self.client.get(reverse('review:product_reviews', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good')
