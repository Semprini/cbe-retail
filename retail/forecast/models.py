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
    

class ProductSaleWeek(models.Model):
    end_date = models.DateField()
    store = models.ForeignKey(Store, related_name='sales_weekly')
    product = models.ForeignKey(Product, related_name='sales_weekly')
    merch_week = models.ForeignKey(MerchWeek, related_name='merch_weeks', null=True, blank=True)
    
    quantity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    on_hand = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    on_order = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    retail_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    average_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    

class ProductForecast(models.Model):
    division = models.CharField(max_length=100, db_index=True)
    merch_week = models.ForeignKey(MerchWeek, related_name='product_forecasts')
    product = models.ForeignKey(Product, related_name='product_forecasts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)