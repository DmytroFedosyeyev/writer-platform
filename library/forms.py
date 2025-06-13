from .models import Rating, Comment
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
