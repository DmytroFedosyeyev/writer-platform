from .models import Rating, Comment, Work
from django import forms

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'placeholder': 'Оценка от 1 до 5'
            })
        }
        labels = {
            'score': 'Ваша оценка'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите ваш комментарий'
            })
        }
        labels = {
            'text': 'Комментарий'
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'genre', 'content']
        labels = {
            'title': 'Название',
            'genre': 'Жанр',
            'content': 'Текст произведения',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название произведения',
                'style': 'width: 100%; height: 40px; font-size: 16px;'  # Увеличенная высота и ширина
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 50%; height: 50px; font-size: 16px;'  # Увеличенная высота
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,  # Увеличено количество строк для текста
                'placeholder': 'Введите текст произведения',
                'style': 'width: 100%; height: 400px; font-size: 16px;'  # Увеличенная высота и ширина
            }),
        }