# userprofiles/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number',)