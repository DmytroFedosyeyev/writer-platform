# Writer Platform

Writer Platform — это веб-приложение для публикации литературных произведений, оценки и комментирования текстов, а также взаимодействия между авторами и читателями.

## Описание проекта

Проект состоит из двух основных приложений:

- users — управление пользователями: регистрация, вход, редактирование, фото профиля
- library — публикация произведений, комментарии, рейтинги, фильтрация, экспорт в PDF

## Функциональность

- Регистрация и вход
- Личный кабинет пользователя
- Загрузка и отображение фото автора
- Добавление, редактирование и удаление произведений
- Оценка произведений по 100-балльной шкале
- Оставление комментариев
- Поиск по названию, жанру, автору
- Отдельная страница с Топ-50 произведениями
- Пагинация текста произведений
- Экспорт текста в PDF
- Удаление аккаунта

## Технический стек

- Python 3.11
- Django 5.2
- MySQL
- HTML, CSS, JavaScript
- CKEditor
- ReportLab

## Требования

- Python 3.11
- MySQL Server
- Git (по желанию)
- Виртуальное окружение (рекомендуется)

## Установка и запуск проекта локально

1. Клонировать репозиторий: https://github.com/DmytroFedosyeyev/writer-platform

2. Создать и активировать виртуальное окружение:

Для Windows: python -m venv .venv
.venv\Scripts\activate

Для Linux или macOS:python3 -m venv .venv
source .venv/bin/activate

3. Установить зависимости: pip install -r requirements.txt

4. Настроить файл .env (если используется):
EMAIL_HOST_USER=ваш_email@gmail.com
EMAIL_HOST_PASSWORD=ваш_пароль

5. Настроить подключение к базе данных в файле settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'writer_platform',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

6. Выполнить миграции:
python manage.py makemigrations
python manage.py migrate

7. Создать суперпользователя: python manage.py createsuperuser

8. Запустить сервер: python manage.py runserver

9. Перейти по адресу: http://127.0.0.1:8000/

Ссылка на развернутое приложение: https://dmytrofedosyeyev.pythonanywhere.com/ 

Автор
Dmytro Fedosyeyev
fedoseevdv1975@gmail.com
