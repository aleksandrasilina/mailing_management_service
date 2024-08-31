import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Здравствуйте, вы зарегистрированы на нашем сайте {host}.'
                    f'Пожалуйста, подтвердите свою почту, перейдя по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            password = User.objects.make_random_password(12)
            user.set_password(password)
            user.save()

            host = self.request.get_host()
            send_mail(
                subject='Восстановление пароля',
                message=f'Здравствуйте, ваш новый пароль для сайта {host}:\n'
                        f'{password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        except Http404:
            form.add_error(None, 'Пользователь с такой почтой не был зарегистрирован')
            return self.form_invalid(form)
        else:
            return redirect(reverse('users:password-reset-done'))
