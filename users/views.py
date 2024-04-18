import string
import random

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, FormView

from users.forms import UserRegisterForm, ProfileChangeForm, CustomAuthenticationForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm')
    extra_context = {
        'title': "Регистрация"
    }

    def form_valid(self, form):
        new_user = form.save()

        new_user.is_active = False
        current_site = self.request.get_host()
        verification_code = ''.join(str(random.randint(0, 9)) for _ in range(8))
        new_user.verification_code = verification_code

        subject = "Подтвердите регистрацию на Skystore"
        message = (f"Для завершения регистрации перейдите по ссылке http://{current_site}/users/confirm/ "
                   f"Ваш код регистрации - {verification_code}")
        new_user.save()

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False,
        )
        new_user.save()
        return super().form_valid(form)


class ConfirmRegisterView(TemplateView):
    model = User
    extra_context = {
        'title': "Подтверждение регистрации"
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'users/confirm_registration.html')

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        user = get_object_or_404(User, verification_code=verification_code)

        if user:
            user.is_active = True
            user.save()
            return redirect('users:login')
        return redirect('catalog:home')


class CustomLoginView(LoginView):
    model = User
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {
        'title': "Вход"
    }


class ProfileView(UpdateView):
    model = User
    form_class = ProfileChangeForm
    # template_name = 'users/set_random_password.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': "Профиль пользователя"
    }

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': "Сброс пароля"
    }

    # def get_object(self, queryset=None):
    #     return self.request.user

    @staticmethod
    def generate_random_password():
        characters = list(string.ascii_letters + string.digits)
        length = 12
        random.shuffle(characters)
        password_list = []
        for i in range(length):
            password_list.append(random.choice(characters))
        random.shuffle(password_list)
        password = "".join(password_list)
        return password

    def form_valid(self, form):
        new_pass = self.generate_random_password()
        email = form.cleaned_data['email']

        for user in form.get_users(email):
            user.set_password(new_pass)
            user.save()

        # password = make_password(new_pass)

        send_mail(
            subject="Сброс пароля",
            message=f"Вы успешно сбросили свой пароль на Skystore! Ваш новый пароль - {new_pass}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return super().form_valid(form)
