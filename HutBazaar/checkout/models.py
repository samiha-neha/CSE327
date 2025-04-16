from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.


class Order(models.Model):
    """Represents a customer order in the system."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    email = models.EmailField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default="pending")
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    discount_coupon_used = models.ForeignKey(
        "Discount",  # Reference to Discount model
        on_delete=models.SET_NULL,  # Keep order if discount is deleted
        null=True,
        blank=True,
    )

    def __str__(self):
        """String representation of the order."""
        return f"Order #{self.id}"

    @property
    def discount_amount(self):
        """
        Calculates the discount amount to be applied without saving anything in database

        Args:
            self: the model in database

        Returns:
           Decimal: the calculated discount considering:
                - Percentage discounts (capped at max_amount)
                - Fixed amount discounts (capped at max_amount)
                - Returns 0 if no discount applies

        Notes:
            If percentage discount higher than max amount, then max amount is returned
            If exact amount is set but higher than max amount, then max amount is returned

        Example:
            For a 10% discount on $100 order with $8 max:
            >>> order.total = 100
            >>> order.discount_coupon_used.amount = 10
            >>> order.discount_coupon_used.max_amount = 8
            >>> order.discount_amount will be = 8
            so returns 8
        """
        if self.discount_coupon_used:
            if self.discount_coupon_used.discount_type == "percentage":
                return min(
                    (self.total * self.discount_coupon_used.amount / 100),
                    self.discount_coupon_used.max_amount,
                )
            # if exact discount amount is set
            return min(
                self.discount_coupon_used.amount, self.discount_coupon_used.max_amount
            )
        return 0

    @property
    def final_total(self):
        """
        Calculates the final total after applying discounts.

        Returns:
            Decimal: The order total minus any applicable discounts
        """
        return self.total - self.discount_amount


class Discount(models.Model):
    """
    Represents a discount coupon that can be applied to orders."""

    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=10, choices=[("percentage", "Percentage"), ("fixed", "Fixed Amount")]
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    max_amount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        """String representation of the discount."""
        return self.code

    def is_used_by_user(self, user):
        """
        Checks if this discount has been used by a specific user.

        Args:
            user (User): The user to check

        Returns:
            bool: True if user has already used this discount, False otherwise
        """
        if user == None:
            return False
        if not user.is_authenticated:
            return False
        return Order.objects.filter(user=user, discount_coupon_used=self).exists()

    def is_valid_for_user(self, user):
        """
        Checks if this discount is valid for a specific user.

        Args:
            user (User): The user to validate against

        Returns:
            bool: True if discount is active, within validity dates,
                  and not already used by this user
        """
        now = timezone.now()
        return (
            self.active
            # current time in between valid from and to
            and self.valid_from <= now <= self.valid_to
            and (not self.is_used_by_user(user))
        )
