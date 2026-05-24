FROM python:3.12-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаём скрипт запуска, который выполнит миграции
RUN echo '#!/bin/bash\n\
python manage.py makemigrations --noinput\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
exec gunicorn cookbook.wsgi:application --bind 0.0.0.0:10000' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
