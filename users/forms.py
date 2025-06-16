from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    display_name = forms.CharField(
        label='Отображаемое имя автора',
        max_length=150,
        required=True,
        help_text='Это имя будет отображаться рядом с вашими произведениями'
    )

    class Meta:
        model = User
        fields = ['username', 'display_name', 'password1', 'password2']
