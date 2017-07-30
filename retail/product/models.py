from django.db import models

from cbe.party.models import Organisation
from cbe.location.models import Location
from cbe.supplier_partner.models import Supplier, Buyer

from retail.store.models import Store
from retail.market.models import MarketSegment, MarketStrategy


class ProductCategory(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    parent = models.ForeignKey('ProductCategory', null=True,blank=True)

    level = models.CharField(max_length=200, choices=(('department', 'department'), ('subdepartment', 'subdepartment'), ('fineline', 'fineline'), ))
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

        
class Product(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    sku = models.CharField(max_length=200)
    bundle = models.ManyToManyField('Product', blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name
    

class ProductOffering(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')

    product = models.ForeignKey(Product)
    
    channels = models.ManyToManyField('sale.SalesChannel', blank=True)
    segments = models.ManyToManyField(MarketSegment, blank=True)
    strategies = models.ManyToManyField(MarketStrategy, blank=True)
    
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    supplier_code = models.CharField(max_length=200, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, null=True, blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return "%s" %(self.product.name)

        
class ProductStockLevel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, related_name='product_stock_levels')
    store = models.ForeignKey(Store)
    location = models.ForeignKey(Location, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    average = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    def __str__(self):
        return "%s:%d"%(self.product.name, self.amount)
    
