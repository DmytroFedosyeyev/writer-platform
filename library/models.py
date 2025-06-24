from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField

# Модель произведения, представляющая литературное произведение
class Work(models.Model):
    GENRE_CHOICES = [
        ('fantasy', 'Фантастика'),
        ('detective', 'Детектив'),
        ('thriller', 'Триллер'),
        ('history', 'История'),
        ('poetry', 'Поэзия'),
        ('drama', 'Драма'),
        ('other', 'Другое'),
    ]
    # Название произведения, ограничено 255 символами
    title = models.CharField(max_length=255)
    # Жанр произведения, выбор из предопределённых вариантов
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    # Содержимое произведения с поддержкой форматированного текста
    content = RichTextField()
    # Дата и время публикации, устанавливается автоматически при создании
    published_date = models.DateTimeField(auto_now_add=True)
    # Автор произведения, связь с пользователем, может быть NULL при удалении автора
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        # Строковое представление модели — название произведения
        return self.title

# Модель комментария к произведению
class Comment(models.Model):
    # Автор комментария, связь с пользователем, может быть NULL при удалении
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Произведение, к которому относится комментарий
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments')
    # Текст комментария, длинное текстовое поле
    text = models.TextField()
    # Дата и время создания комментария, устанавливается автоматически
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Строковое представление модели — имя пользователя и название произведения
        return f'Комментарий от {self.user.username} к "{self.work.title}"'

# Модель рейтинга произведения
class Rating(models.Model):
    # Автор оценки, связь с пользователем, удаление пользователя удаляет оценку
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Произведение, к которому относится оценка
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='ratings')
    # Оценка в диапазоне от 0 до 100
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        # Ограничение: один пользователь может оставить только одну оценку на произведение
        unique_together = ('user', 'work')

    def __str__(self):
        # Строковое представление модели — оценка, имя пользователя и название произведения
        return f'{self.score} от {self.user.username} за "{self.work.title}"'