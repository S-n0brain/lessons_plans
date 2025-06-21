from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            "class": "form-control ",
            "placeholder": "Email",
            "aria-label": "Email"
        })
        self.fields['password1'].widget.attrs.update({
            "class": "form-control mx-2",
            "placeholder": "Пароль",
            "aria-label": "Пароль"
        })
        self.fields['password2'].widget.attrs.update({
            "class": "form-control mx-2",
            "placeholder": "Повторите пароль",
            "aria-label": "Повторите пароль"
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"name": "username", "class": "form-control mx-2",
                                               "placeholder": "Имя пользователя", "aria-label": "Имя пользователя"})
        }
