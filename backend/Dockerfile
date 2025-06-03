FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# Запуск Gunicorn
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]