from django.db import models
from django.contrib.auth.models import User

# Модель профиля пользователя, связанная с пользователем 1:1 для хранения дополнительной информации
class UserProfile(models.Model):
    # Связь с пользователем, удаление пользователя удаляет профиль
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Поле для хранения фотографии пользователя, может быть пустым
    photo = models.ImageField(upload_to='author_photos/', blank=True, null=True)

    class Meta:
        # Указывает кастомное имя таблицы в базе данных
        db_table = 'users_profile'

    def __str__(self):
        # Строковое представление модели — имя пользователя с суффиксом 's profile'
        return f"{self.user.username}'s profile"