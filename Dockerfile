# 1. Берем чистую, стабильную версию Python
FROM python:3.12-slim

# 2. (САМЫЙ ВАЖНЫЙ ШАГ) Устанавливаем системные библиотеки
#    Это "строительные блоки", которые нужны psycopg2 для сборки и работы
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean

# 3. Говорим Python не буферизировать вывод (чтобы логи в Render были "живыми")
ENV PYTHONUNBUFFERED=1

# 4. Создаем рабочую папку для проекта внутри контейнера
WORKDIR /app

# 5. Сначала копируем только файл с зависимостями (это умный шаг для кеширования)
COPY requirements.txt .

# 6. Устанавливаем все Python-библиотеки из вашего requirements.txt
#    Теперь у psycopg2 есть всё, что нужно для успешной установки!
RUN pip install --no-cache-dir -r requirements.txt

# 7. Копируем остальной код проекта в контейнер
COPY . .

# 8. (КРИТИЧНО ДЛЯ БАЗЫ ДАННЫХ) Запускаем миграции и собираем статику
#    Это произойдет во время сборки образа, а не при запуске.
#    Это гарантирует, что структура базы данных будет готова сразу.
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# 9. Запускаем сервер
#    Важно: 'cookbook' — это имя папки с вашим файлом wsgi.py.
#    Если ваша папка называется иначе (например, 'config' или 'mysite'), замените ее.
CMD ["gunicorn", "cookbook.wsgi:application", "--bind", "0.0.0.0:10000"]
