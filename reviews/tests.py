"""Unit tests for the reviews app."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product
from reviews.models import Review


class ReviewModelTest(TestCase):
    """
    Test cases for the Review model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and product for all model tests.
        """
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.product = Product.objects.create(
            name='Test Product',
            price=9.99,
            description='Test Description'
        )

    def test_review_str_representation(self):
        """
        Test the string representation of the Review model.
        """
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Great product!'
        )
        expected_str = f"Review by {self.user.username} for {self.product.name}"
        self.assertEqual(str(review), expected_str)

    def test_stars_property(self):
        """
        Test the stars property returns correct star representation.
        """
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment='Average'
        )
        self.assertEqual(review.stars, '★★★☆☆')

    def test_unique_review_constraint(self):
        """
        Test that a user cannot leave multiple reviews on the same product.
        """
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='First review'
        )
        with self.assertRaises(Exception):
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=4,
                comment='Duplicate review'
            )


class ReviewViewTest(TestCase):
    """
    Test cases for the review views.
    """

    def setUp(self):
        """
        Set up a user, client, and product for testing.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Product X',
            price=20.00,
            description='Product description'
        )
        self.review_url = reverse('reviews:add_review', args=[self.product.id])
        self.product_detail_url = reverse(
            'store:product-detail', kwargs={'pk': self.product.id}
        )

    def test_add_review_unauthenticated_redirect(self):
        """
        Test that unauthenticated users are redirected to the login page.
        """
        response = self.client.post(self.review_url, {
            'rating': 5,
            'comment': 'Nice product'
        })
        self.assertRedirects(
            response, f'/accounts/login/?next={self.review_url}'
        )

    def test_add_review_authenticated_user(self):
        """
        Test that authenticated users can add a review.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.review_url, {
            'rating': 4,
            'comment': 'Very nice!'
        }, follow=True)
        self.assertRedirects(response, self.product_detail_url)
        review = Review.objects.get(product=self.product, user=self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Very nice!')

    def test_update_existing_review(self):
        """
        Test that an existing review is updated instead of duplicated.
        """
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment='Old comment'
        )
        self.client.login(username='testuser', password='testpass123')
        self.client.post(self.review_url, {
            'rating': 5,
            'comment': 'Updated comment'
        })
        review = Review.objects.get(product=self.product, user=self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Updated comment')
        self.assertEqual(Review.objects.count(), 1)

    def test_delete_review_owner(self):
        """
        Test that a user can delete their own review.
        """
        self.client.login(username='testuser', password='testpass123')
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='To be deleted'
        )
        delete_url = reverse('reviews:delete_review', args=[review.id])
        response = self.client.post(delete_url)
        self.assertRedirects(response, self.product_detail_url)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_delete_review_non_owner_fails(self):
        """
        Test that a user cannot delete someone else's review.
        """
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        review = Review.objects.create(
            product=self.product,
            user=other_user,
            rating=2,
            comment='Not yours'
        )
        self.client.login(username='testuser', password='testpass123')
        delete_url = reverse('reviews:delete_review', args=[review.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(id=review.id).exists())

    def test_product_reviews_view(self):
        """
        Test that the product reviews view displays reviews correctly.
        """
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Excellent!'
        )
        url = reverse('reviews:product_reviews', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Excellent!')
        self.assertTemplateUsed(response, 'reviews/product_reviews.html')