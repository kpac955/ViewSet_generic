# LMS Project (HW 30.1)

## Описание
API для системы управления обучением (курсы и уроки).

## Технологический стек
* **Backend:** Django 6.0.2, Django REST Framework 3.17.1
* **Database:** PostgreSQL 15
* **Task Queue:** Celery 5.6.3 + Redis 7
* **Infrastructure:** Docker, Docker Compose

## Запуск через Docker

Проект полностью контейнеризирован. Все зависимости, база данных (PostgreSQL) и брокер сообщений (Redis) настраиваются автоматически.

### 1. Подготовка окружения
Создайте файл `.env` в корне проекта и заполните его данными из `.env.sample`.

### 2. Запуск сервисов
Для сборки образов и запуска всех контейнеров выполните:
```
docker compose up --build
```

### 3. Настройка приложения (выполняется в новом окне терминала)
Примените миграции и создайте администратора для доступа к API (чтобы избежать ошибки 403):
```
docker compose exec app python manage.py migrate
docker compose exec app python manage.py createsuperuser
```

### 4. Проверка работы
API: http://localhost:8000/
Тесты: 
```
docker compose exec app python manage.py test
```
Celery Ping:
```
docker compose exec worker celery -A config inspect ping
```
ожидаем ответ `pong`


## Локальный запуск (без Docker)
1. Клонировать репозиторий: `git clone https://github.com/kpac955/ViewSet_generic.git`
2. Установить зависимости: `pip install -r requirements.txt`.
3. Применить миграции: `python manage.py migrate`.
4. Создать суперпользователя: `python manage.py createsuperuser`.
5. Запустить сервер: `python manage.py runserver`.

**Запуск Celery (Windows):**
* Воркер: `celery -A config worker -l info --pool=solo`
* Планировщик: `celery -A config beat -l info`