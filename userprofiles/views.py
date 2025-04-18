# userprofiles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Note: No direct Order import needed now unless showing order history
from .models import UserProfile
from .forms import UserEditForm, UserProfileEditForm

@login_required
def profile_view(request):
    # Get or create the profile automatically when viewed
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Optional: Fetch order history if you add an 'orders' app later
    # user_orders = request.user.orders.all() # Assumes related_name='orders' on Order model

    context = {
        'user_profile': user_profile,
        # 'user_orders': user_orders, # Uncomment if showing orders
    }
    return render(request, 'userprofiles/profile_detail.html', context)

@login_required
def profile_edit_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = UserProfileEditForm(request.POST, instance=user_profile)
            password_form = PasswordChangeForm(request.user) # Keep for context

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile details updated.')
                return redirect('userprofiles:profile')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            user_form = UserEditForm(instance=request.user) # Keep for context
            profile_form = UserProfileEditForm(instance=user_profile) # Keep for context

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) # Keep user logged in
                messages.success(request, 'Password updated successfully.')
                return redirect('userprofiles:profile')
            else:
                messages.error(request, 'Please correct the password errors below.')
        else: # Should not happen with named buttons
             user_form = UserEditForm(instance=request.user)
             profile_form = UserProfileEditForm(instance=user_profile)
             password_form = PasswordChangeForm(request.user)
             messages.warning(request, 'Invalid form submission.')

    else: # GET request
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=user_profile)
        password_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'userprofiles/profile_edit.html', context)