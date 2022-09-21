from django.urls import path, include
from .views import UserProfileUpdate, upgrade_user, add_subscribe, remove_subscribe

urlpatterns = [
    path('', include('allauth.urls')),
    path('<int:pk>/update/', UserProfileUpdate.as_view(), name='account_profile'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
    path('subscribe/<int:pk>', add_subscribe, name='account_add_sub'),
    path('unsubscribe/<int:pk>', remove_subscribe, name='account_remove_sub'),
]
