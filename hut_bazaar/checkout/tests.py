from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, Discount
from .views import checkout_view
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

"""
Method                          | What it does
self.assertEqual(a, b)          | Passes if a == b
self.assertTrue(x)              | Passes if x is True
self.assertFalse(x)             | Passes if x is False
self.assertRaises(Exception)    | Tests if code raises a certain error (like ValueError)
"""


# Create your tests here.
class OrderModelTest(TestCase):
    def setUp(self):
        # Set up reusable objects
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@gmail.com"
        )
        self.order = Order.objects.create(
            user=self.user,
            email="test@gmail.com",
            total=100.00,
            payment_method="bkash",
            shipping_address="ramapura",
            shipping_city="dhaka",
            shipping_state="dhaka",
            shipping_zip="1219",
        )

        self.percentage_discount = Discount.objects.create(
            code="PERCENT20",
            discount_type="percentage",
            amount=20,
            max_amount=50,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1),
            active=True,
        )

    # These are individual test cases. Django automatically runs all methods starting with test_.
    def test_order_creation(self):
        """Tests if the user and total cost of order are accurate"""
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.total, 100.00)

    def test_str_representation(self):
        """Test the string representation of the order"""
        self.assertTrue(str(self.order).startswith("Order #"))

    def test_percentage_discount(self):
        """Test percentage discount calculation"""
        self.order.discount_coupon_used = self.percentage_discount
        # 20% of 100 = 20
        self.assertEqual(self.order.discount_amount, Decimal("20.00"))


class DiscountModelTest(TestCase):
    def setUp(self):
        """Create test data that will be used across multiple tests"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create test discount
        self.discount = Discount.objects.create(
            code="TEST20",
            discount_type="percentage",
            amount=20,
            max_amount=50,
            valid_from=timezone.now() - timedelta(days=1),  # set days = 2 for expired
            valid_to=timezone.now()
            + timedelta(days=1),  # set  - timedelta(days=1) for expired
            active=True,
        )

    # Test basic model functionality
    def test_discount_creation(self):
        """Test that discount is created with correct attributes"""
        self.assertEqual(self.discount.code, "TEST20")
        self.assertEqual(self.discount.discount_type, "percentage")
        self.assertEqual(self.discount.amount, 20)
        self.assertEqual(self.discount.max_amount, 50)
        self.assertTrue(self.discount.active)

    def test_str_representation(self):
        """Test the string representation of the discount"""
        self.assertEqual(str(self.discount), "TEST20")

    # Test is_used_by_user method
    def test_discount_not_used_by_user(self):
        """Test that discount shows as unused when user hasn't used it"""
        self.assertFalse(self.discount.is_used_by_user(self.user))

    def test_discount_used_by_user(self):
        """Test that discount shows as used if user had previously ordered with it"""
        Order.objects.create(
            user=self.user,
            email=self.user.email,
            total=100,
            shipping_address="ramapura",
            shipping_city="dhaka",
            shipping_state="dhaka",
            shipping_zip="1219",
            discount_coupon_used=self.discount,
        )
        self.assertTrue(self.discount.is_used_by_user(self.user))

    def test_is_valid_for_user(self):
        """Test if discount is is valid for user in terms of previously used and its validity date"""
        self.assertTrue(self.discount.is_valid_for_user(self.user))
