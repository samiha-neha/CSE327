from django.db import models
from django.conf import settings


# Create your models here.
class Order(models.Model):
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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def discount_amount(self):
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
        return self.total - self.discount_amount


class Discount(models.Model):
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
        return self.code
