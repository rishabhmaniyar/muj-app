from django.db import models


# Create your models here.
class Levels(models.Model):
    symbol = models.CharField(max_length=255, unique=False)
    option_type = models.CharField(max_length=255, null=True)
    transaction_type = models.CharField(max_length=255, null=True)
    expiry = models.CharField(max_length=255, null=True)
    strike = models.CharField(max_length=255, null=True)
    qty = models.IntegerField(null=False)
    underlying_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    option_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    sl_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    underlying_sl_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    target_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    underlying_target_price = models.DecimalField(decimal_places=2,max_digits=8,null=True)
    isActive = models.BooleanField(null=False)
