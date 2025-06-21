from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserSignUpForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm


class UserLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="lesson_planner:index")
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Выход"
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="lesson_planner:index")
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    template_name = "users/sign_up.html"
    success_url = reverse_lazy("users:login")
    form_class = UserSignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["form"] = self.get_form(self.form_class)
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="lesson_planner:index")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сменить пароль"
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="lesson_planner:index")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пароль изменён"
        return context


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Восстановление пароля"
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="lesson_planner:index")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Восстановление пароля"
        return context


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Смена пароля"
        print(self.form_class)
        print(self.form_class.base_fields)
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пароль изменён"
        return context
