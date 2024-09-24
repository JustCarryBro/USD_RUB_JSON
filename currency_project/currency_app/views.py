from django.http import JsonResponse
from .models import ExchangeRateRequest
from .tasks import fetch_exchange_rate

def get_current_usd(request):
    fetch_exchange_rate()
    last_requests = list(ExchangeRateRequest.objects.all()[:10].values('rate', 'timestamp'))

    if last_requests:
        current_rate = last_requests[0]['rate']
    else:
        current_rate = None

    return JsonResponse({
        'current_usd_to_rub': current_rate,
        'last_requests': last_requests,
    })