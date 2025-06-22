from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Rating, Comment, Work


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'class': 'score-input',
                'placeholder': '0-100'
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
                'style': 'width: 100%; height: 40px; font-size: 16px;'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 50%; height: 50px; font-size: 16px;'
            }),
            'content': CKEditorWidget(),
        }
