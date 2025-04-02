from django.db import models
from django.conf import settings
from checkout.models import Order  # Import from checkout app


class OrderConfirmation(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="confirmation"
    )
    email_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    email_content = models.TextField(blank=True)

    def __str__(self):
        return f"Confirmation for Order #{self.order.id}"

    class Meta:
        verbose_name = "Order Confirmation"
        verbose_name_plural = "Order Confirmations"
