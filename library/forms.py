from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Rating, Comment, Work

# Форма для создания и редактирования рейтинга произведения
class RatingForm(forms.ModelForm):
    class Meta:
        # Указывает модель, с которой связана форма
        model = Rating
        # Поля формы, доступные для редактирования
        fields = ['score']
        # Настройка виджетов для полей
        widgets = {
            'score': forms.NumberInput(attrs={
                # Ограничения для ввода: от 0 до 100
                'min': 0,
                'max': 100,
                # Дополнительные атрибуты для стилизации и подсказки
                'class': 'score-input',
                'placeholder': '0-100'
            })
        }
        # Кастомные метки для полей
        labels = {
            'score': 'Ваша оценка'
        }

# Форма для создания и редактирования комментария к произведению
class CommentForm(forms.ModelForm):
    class Meta:
        # Указывает модель, с которой связана форма
        model = Comment
        # Поля формы, доступные для редактирования
        fields = ['text']
        # Настройка виджетов для полей
        widgets = {
            'text': forms.Textarea(attrs={
                # Стилизация поля ввода текста
                'class': 'form-control',
                'rows': 4,  # Четыре строки по высоте
                'placeholder': 'Введите ваш комментарий'
            })
        }
        # Кастомные метки для полей
        labels = {
            'text': 'Комментарий'
        }

# Форма для создания и редактирования произведения
class WorkForm(forms.ModelForm):
    class Meta:
        # Указывает модель, с которой связана форма
        model = Work
        # Поля формы, доступные для редактирования
        fields = ['title', 'genre', 'content']
        # Кастомные метки для полей
        labels = {
            'title': 'Название',
            'genre': 'Жанр',
            'content': 'Текст произведения',
        }
        # Настройка виджетов для полей
        widgets = {
            'title': forms.TextInput(attrs={
                # Стилизация поля ввода названия
                'class': 'form-control',
                'placeholder': 'Введите название произведения',
                'style': 'width: 100%; height: 40px; font-size: 16px;'
            }),
            'genre': forms.Select(attrs={
                # Стилизация выпадающего списка жанров
                'class': 'form-control',
                'style': 'width: 50%; height: 50px; font-size: 16px;'
            }),
            'content': CKEditorWidget(),  # Использование CKEditor для редактирования текста
        }