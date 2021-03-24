from django.urls import path
from .views import *
from django.contrib.auth.views import (PasswordChangeView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView, LoginView, LogoutView)

app_name = 'user'
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('activation/sent/', activation_sent, name='activation_sent'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
