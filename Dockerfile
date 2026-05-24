FROM python:3.12-slim

RUN apt-get update && apt-get -y install libpq-dev gcc && apt-get clean

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Делаем скрипт запуска исполняемым
RUN chmod +x start.sh

# Запускаем через start.sh, который выполнит миграции
CMD ["./start.sh"]
