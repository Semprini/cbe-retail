from django.db import models

from cbe.party.models import Organisation
from cbe.location.models import AbsoluteLocalLocation
from cbe.customer.models import Customer
from cbe.supplier_partner.models import Supplier, Buyer

from retail.market.models import MarketSegment, MarketStrategy


class ProductCategory(models.Model):
    parent = models.ForeignKey('ProductCategory', null=True,blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    level = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductOffering(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.TextField()
    supplier_code = models.TextField(null=True, blank=True)
    bundle = models.ManyToManyField('ProductOffering', blank=True)
    unit_of_measure = models.CharField(max_length=200)

    channels = models.ManyToManyField('sale.RetailChannel', blank=True)
    categories = models.ManyToManyField('ProductCategory', blank=True)
    segments = models.ManyToManyField(MarketSegment, blank=True)
    strategies = models.ManyToManyField(MarketStrategy, blank=True)
    
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, null=True, blank=True)

    def __str__(self):
        return self.name

        
class ProductOfferingPrice(models.Model):
    product_offering = models.ForeignKey(ProductOffering, related_name='product_offering_prices')
    promotion = models.ForeignKey('Promotion', null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField('ProductCategory', blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    
class ProductStockLevel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    product_offering = models.ForeignKey(ProductOffering)
    store = models.ForeignKey(Organisation)
    location = models.ForeignKey(AbsoluteLocalLocation, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    average = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    
class Promotion(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField('ProductCategory', blank=True)
    products = models.ManyToManyField('ProductOffering', blank=True)
    customers = models.ManyToManyField(Customer, blank=True)

    def __str__(self):
        return self.name
