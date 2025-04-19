"""Test cases for the cart application views and models."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from store.models import Product, Category
from .models import Cart, CartItem


class CartTests(TestCase):
    """Test suite for cart functionality."""

    def setUp(self):
        """Create test data that will be used across all test cases."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()

        # Create required category - adjust fields to match your actual Category model
        self.category = Category.objects.create(
            name='Test Category'
            # Remove 'slug' if your model doesn't have it
            # Add any other required fields your Category model needs
        )

        # Create test product with valid category
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='Test description',
            category=self.category,
            # Add any other required fields your Product model needs
        )

        # Create cart for the user
        self.cart = Cart.objects.create(user=self.user)

        # Log in the test user
        self.client.login(username='testuser', password='testpass123')

    def test_add_to_cart(self):
        """Test adding a product to the cart."""
        self.assertEqual(CartItem.objects.count(), 0)
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_increases_quantity(self):
        """Test that adding same product twice increases quantity."""
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]))
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]))
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        """Test removing an item from the cart."""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        response = self.client.post(
            reverse('cart:remove_from_cart', args=[cart_item.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart:view_cart'))
        self.assertEqual(CartItem.objects.count(), 0)

    def test_update_quantity(self):
        """Test updating the quantity of a cart item."""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        response = self.client.post(
            reverse('cart:update_quantity', args=[cart_item.id]),
            {'quantity': 3}
        )
        self.assertEqual(response.status_code, 302)
        updated_item = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated_item.quantity, 3)