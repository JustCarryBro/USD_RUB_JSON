from django.utils import timezone
from datetime import timedelta
import requests
from celery import shared_task
from .models import ExchangeRateRequest

@shared_task
def fetch_exchange_rate():
    last_request = ExchangeRateRequest.objects.order_by('-timestamp').first()
    if last_request:
        time_since_last_request = timezone.now() - last_request.timestamp
        if time_since_last_request < timedelta(seconds=10):
            return
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)

            rate = data['Valute']['USD']['Value']

            # Сохраняем в базе данных
            ExchangeRateRequest.objects.create(rate=rate)
            return rate
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")  # Логируем ошибку запроса
        raise ValueError("Ошибка при выполнении запроса к API")