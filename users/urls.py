from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Набор маршрутов для управления пользователями и аутентификацией
urlpatterns = [
    # Регистрация нового пользователя
    path('signup/', views.signup_view, name='signup'),
    # Вход пользователя в систему с кастомным шаблоном
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Выход пользователя с перенаправлением на главную страницу
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Домашняя страница авторизованного пользователя
    path('home/', views.home_view, name='user_home'),
    # Просмотр профиля пользователя по имени
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

    # Маршруты для восстановления пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),  # Запрос на сброс пароля
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),  # Подтверждение отправки инструкций
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),  # Подтверждение нового пароля
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),  # Завершение сброса пароля
]