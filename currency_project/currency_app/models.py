from django.db import models

class ExchangeRateRequest(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Запросы обменного курса"