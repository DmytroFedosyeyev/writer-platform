from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('user_home')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def home_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Профиль обновлён!')
        return redirect('user_home')
    return render(request, 'users/user_home.html', {'user': request.user})

def profile_view(request, username):
    user = User.objects.get(username=username)
    if request.user.is_authenticated and request.user.username == username:
        # Если авторизованный пользователь просматривает свой профиль
        return render(request, 'users/user_home.html', {'user': user})
    else:
        # Для гостей или просмотра чужого профиля
        return render(request, 'users/profile.html', {'user': user})