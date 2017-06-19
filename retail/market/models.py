from django.db import models



class MarketSegment(models.Model):
    name = models.CharField(max_length=200)

class MarketStrategy(models.Model):
    name = models.CharField(max_length=200)

