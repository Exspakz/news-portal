from django.urls import path, include
from .views import UserProfileUpdate, upgrade_user

urlpatterns = [
    path('', include('allauth.urls')),
    path('<int:pk>/update/', UserProfileUpdate.as_view(), name='account_profile'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
]
