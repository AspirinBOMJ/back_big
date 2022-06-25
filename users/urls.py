from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('email_activate/<uidb64>/<token>/', ActivateEmailView.as_view(), name='activate_email'),
    path('reset_pass/<uidb64>/<token>/', ResetPasswordChangeView.as_view(), name='reset_pass'),
    path('email_success/', ActivateEmailSuccessView.as_view(), name='email_success'),
    path('email_error/', ActivateEmailErrorView.as_view(), name='email_error'),
    path('email_send/', ActivateEmailSendView.as_view(), name='email_send'),
    path('reset_pass/send_email/<email>/', ResetPasswordSendView.as_view(), name='reset_pass_send'),
    path('reset_pass/look_email/', ResetPassworEmailView.as_view(), name='reset_pass_email'),
    path('change/password/<slug:pk>/', UserChangePasswordView.as_view(), name='change_password'),
    path('change/email/<slug:pk>/', UserChangeEmailView.as_view(), name='change_email'),
    path('reset_pass/error/', ResetPasswordErrorView.as_view(), name='reset_pass_error'),
    path('detail/<slug:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
]
