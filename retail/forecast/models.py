from django.db import models

from retail.product.models import Product


class MerchWeek(models.Model):
    number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    start = models.DateField()
    end = models.DateField()
    
    
class ProductForecast(models.Model):
    division = models.CharField(max_length=100, db_index=True)
    merch_week = models.ForeignKey(MerchWeek, related_name='product_forecasts')
    product = models.ForeignKey(Product, related_name='product_forecasts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)