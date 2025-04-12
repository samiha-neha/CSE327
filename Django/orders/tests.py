# orders/tests.py

import datetime
import uuid  # Keep uuid if tracking_id is used
from django.test import TestCase
from django.utils import timezone # Import timezone for date/time operations
from .models import Order
from decimal import Decimal # Make sure Decimal is imported

class OrderModelTests(TestCase):

    # --- New Tests for Defaults ---

    def test_order_status_defaults_to_pending(self):
        """
        Verify that a new Order defaults to PENDING status.
        """
        # Arrange: Create an order providing only minimal required fields
        # Make sure these fields are actually required by your model
        order = Order.objects.create(
            customer_name="Default Status Test",
            customer_email="default_status@example.com",
            shipping_address="1 Default St"
            # DO NOT specify 'status' here
        )
        # Act: Status is set automatically by the model default
        # Assert
        print(f"\n   Testing {self._testMethodName}: Status={order.status}, Expected='PENDING'")
        self.assertEqual(order.status, Order.OrderStatus.PENDING)

    def test_order_total_amount_defaults_to_zero(self):
        """
        Verify that a new Order defaults to 0.00 total_amount.
        """
        # Arrange: Create an order providing only minimal required fields
        order = Order.objects.create(
            customer_name="Default Amount Test",
            customer_email="default_amount@example.com",
            shipping_address="2 Default St"
            # DO NOT specify 'total_amount' here
        )
        # Act: total_amount is set automatically by the model default
        # Assert
        print(f"\n   Testing {self._testMethodName}: Amount={order.total_amount}, Expected=0.00")
        self.assertEqual(order.total_amount, Decimal('0.00'))

    # --- Existing Tests ---

    def test_order_string_representation(self):
        """
        Test that the string representation of an Order object is correct.
        Assumes __str__ returns f"Order {self.id} ({self.tracking_id})".
        """
        # Arrange: Create an instance using ACTUAL fields from your Order model
        test_uuid = uuid.uuid4()
        # Ensure ALL required fields (those without blank=True, null=True, or default) are provided
        order = Order.objects.create(
            # --- Adjust these fields based on your ACTUAL Order model ---
            customer_name="Test Customer Str",
            customer_email="test_str@example.com",
            shipping_address="123 String St",
            tracking_id=test_uuid, # Assumes you have tracking_id
            order_date=timezone.now(), # Provide a date/time
            total_amount=Decimal('10.00') # Example if you have this field - ensure Decimal()
            # --- End of fields to adjust ---
        )

        # Act: Get the string representation
        order_as_string = str(order)

        # Assert: Check against the expected __str__ output format
        expected_string = f"Order {order.id} ({test_uuid})" # Use the generated id and the uuid used
        print(f"\n   Testing {self._testMethodName}: Got '{order_as_string}', Expected '{expected_string}'") # Debug print
        self.assertEqual(order_as_string, expected_string)

    def test_was_ordered_recently_with_future_order(self):
        """
        was_ordered_recently() should return False for orders whose order_date is in the future.
        """
        # Arrange
        future_date = timezone.now() + datetime.timedelta(days=30)
        # Create order using only necessary fields for the test (and required model fields)
        future_order = Order.objects.create(
             order_date=future_date,
             # Add other REQUIRED fields if Order model needs them for creation
             customer_name="Test Customer Future",
             customer_email="test_future@example.com",
             shipping_address="123 Future St",
             tracking_id=uuid.uuid4() # Provide if required
        )

        # Act
        result = future_order.was_ordered_recently() # Assumes this method exists on Order model

        # Assert
        self.assertIs(result, False)
        print(f"\n   Testing {self._testMethodName}: Date {future_date}, Result={result}, Expected False")

    def test_was_ordered_recently_with_old_order(self):
        """
        was_ordered_recently() should return False for orders whose order_date is older than 1 day.
        """
        # Arrange
        # Define old_date WITHIN this test
        old_date = timezone.now() - datetime.timedelta(days=1, seconds=1) # Clearly older than 1 day
        # Create order using only necessary fields for the test (and required model fields)
        old_order = Order.objects.create(
            order_date=old_date,
            # Add other REQUIRED fields if Order model needs them for creation
            customer_name="Test Customer Old",
            customer_email="test_old@example.com",
            shipping_address="123 Old St",
            tracking_id=uuid.uuid4() # Provide if required
        )

        # Act
        result = old_order.was_ordered_recently() # Assumes this method exists on Order model

        # Assert
        self.assertIs(result, False)
        print(f"\n   Testing {self._testMethodName}: Date {old_date}, Result={result}, Expected False")

    def test_was_ordered_recently_with_recent_order(self):
        """
        was_ordered_recently() should return True for orders whose order_date is within the last day.
        """
        # Arrange
        # Define recent_date WITHIN this test
        recent_date = timezone.now() - datetime.timedelta(hours=23) # Clearly within the last day
        # Create order using only necessary fields for the test (and required model fields)
        recent_order = Order.objects.create(
            order_date=recent_date,
            # Add other REQUIRED fields if Order model needs them for creation
            customer_name="Test Customer Recent",
            customer_email="test_recent@example.com",
            shipping_address="123 Recent St",
            tracking_id=uuid.uuid4() # Provide if required
        )

        # Act
        result = recent_order.was_ordered_recently() # Assumes this method exists on Order model

        # Assert
        self.assertIs(result, True)
        print(f"\n   Testing {self._testMethodName}: Date {recent_date}, Result={result}, Expected True")

# --- You would add the OrderTrackingViewTests and OrderTrackingFormTests classes below this line ---
# class OrderTrackingViewTests(TestCase):
#    ... tests from Step 3 ...

# class OrderTrackingFormTests(TestCase):
#    ... tests from Step 4 (if needed) ...