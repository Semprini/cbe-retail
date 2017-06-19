from django.db import models

from cbe.customer.models import Customer
from cbe.party.models import Organisation

from retail.product.models import ProductOffering, ProductCategory


class PriceChannel(models.Model):
    name = models.CharField(max_length=100)
    
    
class PriceCalculation(models.Model):
    price_channel = models.ForeignKey(PriceChannel)
    name = models.CharField(max_length=100)

    
class Promotion(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField(ProductCategory, blank=True)
    products = models.ManyToManyField(ProductOffering, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    stores = models.ManyToManyField(Organisation, blank=True)

    def __str__(self):
        return self.name

    
class ProductOfferingPrice(models.Model):
    product_offering = models.ForeignKey(ProductOffering, related_name='product_offering_prices')
    promotion = models.ForeignKey(Promotion, null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "%s %s"%( self.product_offering, self.name )
    