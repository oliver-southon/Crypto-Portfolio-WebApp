from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Holding(models.Model):
    trader = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    symbol = models.CharField('Coin Symbol', max_length=20)
    coin_id = models.CharField('Coin ID for API', max_length=50)
    entry_price = models.DecimalField(decimal_places=10, max_digits=15, blank=True)
    entry_amount = models.DecimalField(decimal_places=10, max_digits=15)
    entry_date = models.DateField(auto_now_add=True, blank=True, null=True)
    sold = models.BooleanField(default=False)
    exit_price = models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True)
    exit_date = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.sold:
            return f'{self.symbol} - |BOUGHT: {self.entry_date} / {self.entry_price}|   |SOLD: {self.exit_date} / {self.exit_price}|'
        else:
            return f'{self.symbol} - |BOUGHT: {self.entry_date} / {self.entry_price}|'


