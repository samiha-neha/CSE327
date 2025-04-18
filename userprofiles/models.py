# userprofiles/models.py
from django.db import models
from django.conf import settings # To get AUTH_USER_MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile' # Access via user.profile
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # Add other fields like address, etc., if needed

    def __str__(self):
        return f"Profile for {self.user.username}"