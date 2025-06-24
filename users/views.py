import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

# Настройка логгера для записи событий, связанных с пользователями
logger = logging.getLogger('users')

# Функция обработки регистрации нового пользователя
def signup_view(request):
    logger.info("Запрос на регистрацию нового пользователя")
    if request.method == 'POST':
        # Обработка POST-запроса с формой регистрации
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Сохранение нового пользователя и авторизация
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            logger.info(f"Пользователь {username} успешно зарегистрирован")
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('user_home')
        else:
            logger.error(f"Ошибка валидации формы регистрации: {form.errors}")
    else:
        # Инициализация пустой формы для GET-запроса
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Функция отображения домашней страницы авторизованного пользователя
@login_required
def home_view(request):
    logger.info(f"Запрос на просмотр профиля пользователя {request.user.username}")
    # Получение или создание профиля пользователя
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.FILES.get('photo'):
        try:
            # Обработка загрузки фотографии профиля
            profile.photo = request.FILES['photo']
            profile.save()
            logger.info(f"Фото пользователя {request.user.username} успешно обновлено")
            messages.success(request, "Фото успешно обновлено!")
        except Exception as e:
            # Обработка ошибок при загрузке файла
            logger.error(f"Ошибка при загрузке фото: {e}")
            messages.error(request, f"Ошибка при загрузке фото: {e}")

    return render(request, 'users/user_home.html', {'user': request.user, 'profile': profile})

# Функция отображения профиля пользователя по имени
def profile_view(request, username):
    logger.info(f"Запрос на просмотр профиля пользователя {username}")
    # Получение пользователя по имени
    user = User.objects.get(username=username)
    # Получение или создание профиля пользователя
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.user.is_authenticated and request.user.username == username:
        # Рендеринг страницы для своего профиля
        return render(request, 'users/user_home.html', {'user': user, 'profile': profile})
    else:
        # Рендеринг страницы для просмотра чужого профиля или гостя
        return render(request, 'users/profile.html', {'user': user, 'profile': profile})

# Функция обработки удаления аккаунта пользователя
@login_required
def delete_account_view(request):
    logger.info(f"Запрос на удаление аккаунта пользователя {request.user.username}")
    if request.method == 'POST':
        # Обработка POST-запроса для подтверждения удаления
        user = request.user
        username = user.username
        logout(request)  # Выход из аккаунта перед удалением
        user.delete()
        logger.info(f"Аккаунт пользователя {username} успешно удалён")
        messages.success(request, 'Ваш аккаунт удалён. До свидания!')
        return redirect('home')
    return render(request, 'users/delete_account.html')