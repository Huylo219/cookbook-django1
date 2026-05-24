FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Собираем статику и применяем миграции
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Запускаем сервер
CMD ["gunicorn", "cookbook.wsgi:application", "--bind", "0.0.0.0:10000"]
