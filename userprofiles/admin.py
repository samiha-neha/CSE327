# userprofiles/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Define an inline admin descriptor for UserProfile
class UserProfileInline(admin.StackedInline): # Or TabularInline
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Define a new User admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')
    list_select_related = ('profile',) # Optimize query

    # Method to display phone number from profile in User list
    def get_phone_number(self, instance):
        # Check if profile exists before accessing phone_number
        # Handle cases where profile might not have been created yet
        try:
            return instance.profile.phone_number
        except UserProfile.DoesNotExist:
            return None
    get_phone_number.short_description = 'Phone Number' # Column header

    # Ensure inline only appears for existing users, not when adding a new one
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)