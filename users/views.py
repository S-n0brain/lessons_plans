from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserSignUpForm


class UserLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context


class UserLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Выход"
        return context


class UserCreateView(CreateView):
    template_name = "users/sign_up.html"
    success_url = reverse_lazy("users:login")
    form_class = UserSignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["form"] = self.get_form(self.form_class)
        return context
