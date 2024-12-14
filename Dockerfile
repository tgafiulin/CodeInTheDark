# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и код
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Указываем переменные окружения
ENV PYTHONUNBUFFERED=1

# Указываем порт (например, 8080)
EXPOSE 8080

# Запускаем бота
CMD ["python", "bot.py"]
