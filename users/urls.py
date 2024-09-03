from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, UserPasswordResetView, UserListView, \
    toggle_activity, UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>', email_verification, name='email-confirm'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password-reset-done'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),

]
