FROM python:3.12-slim

# Запрещаем Python писать файлы .pyc и включаем буферизацию логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Системные зависимости для сборки пакетов (нужно для psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Команда для запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]