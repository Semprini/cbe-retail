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

    merch_week = models.ForeignKey(MerchWeek, on_delete=models.CASCADE, related_name='merch_dates')
    

class StoreProductSaleWeek(models.Model):
    end_date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product_sales_weekly')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='store_product_sales_weekly')
    product_txtid = models.CharField(max_length=50)
    merch_week = models.ForeignKey(MerchWeek, on_delete=models.CASCADE, related_name='store_product_sales_weekly_merch_weeks', null=True, blank=True)
    
    quantity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    on_hand = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    on_order = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    retail_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    average_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


class ProductSaleWeek(models.Model):
    end_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='product_sales_weekly')
    product_txtid = models.CharField(max_length=50)
    merch_week = models.ForeignKey(MerchWeek, on_delete=models.CASCADE, related_name='product_sales_weekly_merch_weeks', null=True, blank=True)
    
    store_count = models.IntegerField()
    quantity = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    on_hand = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    on_order = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)

    store_stock_count = models.IntegerField()
    store_sales_count = models.IntegerField()
    

class ProductForecast(models.Model):
    division = models.CharField(max_length=100, db_index=True)
    merch_week = models.ForeignKey(MerchWeek, on_delete=models.CASCADE, related_name='product_forecasts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_forecasts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)