from django.db import models

from retail.product.models import Product
from retail.store.models import Store

class MerchWeek(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    name = models.CharField(max_length=100)

    calendar_start = models.DateField(null=True, blank=True)
    calendar_end = models.DateField()
    calendar_week_number = models.IntegerField()
    
    
class MerchDate(models.Model):
    calendar_date = models.DateField()
    calendar_date_txt = models.CharField(max_length=100)
    calendar_week_end = models.DateField()
    calendar_week_number = models.IntegerField()

    merch_week = models.ForeignKey(MerchWeek, related_name='merch_dates')
    

class ProductStockWeekly(models.Model):
    store = models.ForeignKey(MerchWeek, related_name='product_stock_weekly')
    product = models.ForeignKey(Product, related_name='product_stock_weekly')
    merch_week = models.ForeignKey(MerchWeek, related_name='merch_weeks')
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    

class ProductForecast(models.Model):
    division = models.CharField(max_length=100, db_index=True)
    merch_week = models.ForeignKey(MerchWeek, related_name='product_forecasts')
    product = models.ForeignKey(Product, related_name='product_forecasts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)