# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Форма регистрации (наследуется от встроенной UserCreationForm)
class RegisterForm(UserCreationForm):
    # Добавим поле email, сделаем его обязательным
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма входа — используем стандартную AuthenticationForm, ничего не меняем
class LoginForm(AuthenticationForm):
    pass  # можно оставить пустым, она уже содержит поля username и password
