# Writer Platform

Writer Platform — это веб-приложение, предназначенное для публикации литературных произведений, взаимодействия с другими авторами и читателями, а также оценки и комментирования творчества.

## Функциональность

* Регистрация и вход пользователей
* Личный кабинет (редактирование профиля, загрузка фото, отображение произведений)
* Создание, редактирование и удаление произведений
* Оценки (от 0 до 100) и комментарии
* Поиск и фильтрация по названию, жанру, автору
* Страница TOP-50 по оценкам, комментариям или жанрам
* Пагинация текста произведений
* Экспорт произведения в PDF

## Технический стек

* Python 3.11+
* Django 5.2
* MySQL
* HTML5, CSS3 (custom design, без Bootstrap)
* JavaScript
* CKEditor
* ReportLab (PDF)

## Установка и запуск проекта локально

1. **Клонируйте репозиторий:**

```bash
https://github.com/your_username/writer-platform.git
cd writer-platform
```

2. **Создайте и активируйте виртуальное окружение:**

```bash
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate для Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Если используется .env:**

Создайте файл `.env` в корне проекта (esli нужно):

```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

5. **Примените миграции:**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Создайте суперпользователя:**

```bash
python manage.py createsuperuser
```

7. **Запустите сервер:**

```bash
python manage.py runserver
```

8. **Откройте в браузере:**

```
http://127.0.0.1:8000
```

---

> Проект находится на этапе активной разработки. Если у вас есть предложения или ошибки — смело открывайте issue.

