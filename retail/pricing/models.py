from django.db import models

from cbe.customer.models import Customer, CustomerAccount
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
    product_offerings = models.ManyToManyField(ProductOffering, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    stores = models.ManyToManyField(Organisation, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name

    
class ProductOfferingPrice(models.Model):
    product_offering = models.ForeignKey(ProductOffering, related_name='product_offering_prices')
    promotion = models.ForeignKey(Promotion, null=True, blank=True, related_name='product_offering_prices')
    account = models.ForeignKey(CustomerAccount, null=True, blank=True, related_name='product_offering_prices')
    quote = models.ForeignKey('order.Quote', null=True, blank=True, related_name='product_offering_prices')
    
    #pickslip
    #threshold
    
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)

    mode = models.CharField(max_length=200, choices=(('cost plus', 'cost plus'), ('retail minus', 'retail minus'), ('fixed', 'fixed'), ), default='retail minus')
    mode_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s %s"%( self.product_offering, self.name )
    