from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('email-confirm/<str:token>', email_verification, name='email-confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    # path('password-reset-done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password-reset-done')
]
