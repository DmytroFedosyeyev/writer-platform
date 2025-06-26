from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Кастомная форма для регистрации пользователя с дополнительными полями (имя, фамилия, email)
class CustomUserCreationForm(UserCreationForm):
    # Поле для имени пользователя, обязательное, до 30 символов
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    # Поле для фамилии пользователя, обязательное, до 30 символов
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    # Поле для email, обязательное и с валидацией формата
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        # Указывает модель, с которой связана форма
        model = User
        # Расширяет стандартные поля UserCreationForm дополнительными полями
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        # Переопределяет метод сохранения для обработки дополнительных полей
        user = super().save(commit=False)
        # Установка имени из формы
        user.first_name = self.cleaned_data['first_name']
        # Установка фамилии из формы
        user.last_name = self.cleaned_data['last_name']
        # Установка email из формы
        user.email = self.cleaned_data['email']
        if commit:
            # Сохранение пользователя в базе, если commit=True
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
