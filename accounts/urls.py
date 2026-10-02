from django.urls import path
from .views import (
    RegisterAPIView,
    UserProfileView,
    UserDeleteAPIView,
    ChangePasswordView,
    LogoutView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    # Account ენდპოინტები
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/delete/', UserDeleteAPIView.as_view(), name='delete-account'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),

    # auth (პატარა ასოთი) ჯგუფის ენდპოინტი აღწერით
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),

    # Auth (დიდი ასოთი) ჯგუფის ენდპოინტები
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),

    # api ჯგუფის ენდპოინტი
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]