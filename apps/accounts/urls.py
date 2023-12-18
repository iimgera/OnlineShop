from django.urls import path
from api.auth.auth import (
    RegistrationView, LoginView,
    LogoutView, PasswordResetRequestView,
    OTPVerificationView, CreateNewPasswordView,
)


urlpatterns = [
    path('auth/register/', RegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/otp-verification/', OTPVerificationView.as_view(), name='otp-verification'),
    path('auth/set-new-password/', CreateNewPasswordView.as_view(), name='set-new-password'),
]
