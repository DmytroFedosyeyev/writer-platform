from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


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

    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    content = RichTextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.username} к "{self.work.title}"'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])  # Изменено с 0-5 на 0-100

    class Meta:
        unique_together = ('user', 'work')  # Один пользователь - одна оценка на произведение

    def __str__(self):
        return f'{self.score} от {self.user.username} за "{self.work.title}"'
