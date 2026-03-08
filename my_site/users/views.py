from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохраняем пользователя в БД
            # Автоматически входим после регистрации (опционально)
            login(request, user)
            messages.success(
                request, 'Вы успешно зарегистрировались и вошли в систему.')
            return redirect('homepage')  # перенаправляем на главную
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('homepage')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# Выход
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('homepage')
