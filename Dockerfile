FROM python:3.12-slim

RUN apt-get update && apt-get -y install libpq-dev gcc && apt-get clean

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ЭТОТ СКРИПТ ВЫПОЛНИТ МИГРАЦИИ ПРИ ЗАПУСКЕ
CMD sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn cookbook.wsgi:application --bind 0.0.0.0:10000"
