# userprofiles/urls.py
from django.urls import path
from . import views

app_name = 'userprofiles'

urlpatterns = [
    # Note: Included with /profile/ prefix in main urls.py
    path('', views.profile_view, name='profile'),
    path('edit/', views.profile_edit_view, name='profile_edit'),
]