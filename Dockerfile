# Базовый образ
FROM python:3.12-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запускаем приложение
CMD ["flask", "--app", "Test", "run", "--host=0.0.0.0", "--port=5000"]
