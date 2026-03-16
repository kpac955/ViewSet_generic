# LMS Project (HW 30.1)

## Описание
API для системы управления обучением (курсы и уроки).

## Как запустить
1. Клонировать репозиторий.
2. Установить зависимости: `pip install -r requirements.txt`.
3. Применить миграции: `python manage.py migrate`.
4. Создать суперпользователя: `python manage.py createsuperuser`.
5. Запустить сервер: `python manage.py runserver`.