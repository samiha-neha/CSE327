# orders/tests.py

import datetime
import uuid
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal # Import Decimal for monetary values
from .models import Order # Import the Order model to be tested

# Note: These tests assume the existence of the fields and methods
# defined in the current orders/models.py file.

class OrderModelTests(TestCase):

    def test_order_status_defaults_to_pending(self):
        """
        Verify that a new Order defaults to PENDING status when not specified.
        """
        # Arrange: Create an order providing only fields required by the model
        # (customer_name, customer_email, shipping_address are required)
        order = Order.objects.create(
            customer_name="Default Status Test",
            customer_email="default_status@example.com",
            shipping_address="1 Default St"
            # Status is NOT provided, should use the model default
        )

        # Act: Status is set automatically by the model default
        # Assert: Check if the status matches the expected default from OrderStatus
        self.assertEqual(order.status, Order.OrderStatus.PENDING)

    def test_order_total_amount_defaults_to_zero(self):
        """
        Verify that a new Order defaults to 0.00 total_amount when not specified.
        """
        # Arrange: Create an order providing only required fields
        order = Order.objects.create(
            customer_name="Default Amount Test",
            customer_email="default_amount@example.com",
            shipping_address="2 Default St"
            # total_amount is NOT provided, should use the model default
        )

        # Act: total_amount is set automatically by the model default
        # Assert: Check if the total_amount matches the Decimal('0.00') default
        self.assertEqual(order.total_amount, Decimal('0.00'))

    def test_order_string_representation(self):
        """
        Test that the __str__ method of an Order object returns the expected format.
        """
        # Arrange: Create an instance providing required fields
        # tracking_id is generated automatically, but we can use it in the assertion
        order = Order.objects.create(
            customer_name="Test Customer Str",
            customer_email="test_str@example.com",
            shipping_address="123 String St",
            # order_date and total_amount are optional here since they have defaults,
            # but providing them makes the test object more complete.
            order_date=timezone.now(),
            total_amount=Decimal('10.00')
        )

        # Act: Get the string representation using the model's __str__ method
        order_as_string = str(order)

        # Assert: Check against the expected __str__ output format defined in the model
        expected_string = f"Order {order.id} ({order.tracking_id})"
        self.assertEqual(order_as_string, expected_string)

    def test_was_ordered_recently_with_future_order(self):
        """
        was_ordered_recently() should return False for orders whose order_date
        is set in the future.
        """
        # Arrange: Create a future date and an order with that date
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_order = Order.objects.create(
             order_date=future_date, # Set the date explicitly
             # Provide other required fields
             customer_name="Test Customer Future",
             customer_email="test_future@example.com",
             shipping_address="123 Future St",
        )

        # Act: Call the method under test
        result = future_order.was_ordered_recently()

        # Assert: The result should be False for future dates
        self.assertIs(result, False)

    def test_was_ordered_recently_with_old_order(self):
        """
        was_ordered_recently() should return False for orders whose order_date
        is older than 1 day.
        """
        # Arrange: Create a date older than 1 day and an order with that date
        # Use more than 24 hours to be clearly outside the "recent" window
        old_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_order = Order.objects.create(
            order_date=old_date, # Set the date explicitly
            # Provide other required fields
            customer_name="Test Customer Old",
            customer_email="test_old@example.com",
            shipping_address="123 Old St",
        )

        # Act: Call the method under test
        result = old_order.was_ordered_recently()

        # Assert: The result should be False for old dates
        self.assertIs(result, False)

    def test_was_ordered_recently_with_recent_order(self):
        """
        was_ordered_recently() should return True for orders whose order_date
        is within the last day.
        """
        # Arrange: Create a date within the last 24 hours and an order with that date
        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_order = Order.objects.create(
            order_date=recent_date, # Set the date explicitly
            # Provide other required fields
            customer_name="Test Customer Recent",
            customer_email="test_recent@example.com",
            shipping_address="123 Recent St",
        )

        # Act: Call the method under test
        result = recent_order.was_ordered_recently()

        # Assert: The result should be True for recent dates
        self.assertIs(result, True)

# --- Placeholder for Future Tests ---

# You would add tests for your views here, simulating requests
# class OrderViewTests(TestCase):
#    def test_order_list_view_status_code(self):
#        # Example: response = self.client.get(reverse('orders:order_list'))
#        #          self.assertEqual(response.status_code, 200)
#        pass # Replace with actual view tests
#
#    def test_order_detail_view_content(self):
#        # Example: order = Order.objects.create(...)
#        #          response = self.client.get(reverse('orders:order_detail', args=[order.pk]))
#        #          self.assertContains(response, order.customer_name)
#        pass # Replace with actual view tests

# You would add tests for your forms here, checking validation
# class OrderFormTests(TestCase):
#    def test_valid_form(self):
#        # Example: form_data = {'field1': 'value1', ...}
#        #          form = YourOrderForm(data=form_data)
#        #          self.assertTrue(form.is_valid())
#        pass # Replace with actual form tests
#
#    def test_invalid_form(self):
#        # Example: form_data = {'field1': '', ...} # Invalid data
#        #          form = YourOrderForm(data=form_data)
#        #          self.assertFalse(form.is_valid())
#        pass # Replace with actual form tests