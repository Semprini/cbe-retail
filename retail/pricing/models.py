from django.db import models


class PriceChannel(models.Model):
    name = models.CharField(max_length=100)
    
    
class PriceCalculation(models.Model):
    price_channel = models.ForeignKey(PriceChannel)
    name = models.CharField(max_length=100)
