from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, UserRegisterForm


class RegisterView(CreateView):
    """Регистрация пользователя + отправка приветственного письма."""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        send_mail(
            subject="Добро пожаловать!",
            message=(
                f"Здравствуйте, {user.email}!\n\n"
                "Вы успешно зарегистрировались в нашем магазине. "
                "Рады видеть вас!"
            ),
            from_email="noreply@shop.ru",
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Авторизация по email и паролю."""

    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("catalog:home")


def logout_view(request):
    """Выход из аккаунта."""
    logout(request)
    return redirect("catalog:home")
