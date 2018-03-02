from django.db import models

from cbe.customer.models import Customer, CustomerAccount

from retail.store.models import Store
from retail.product.models import ProductOffering, ProductCategory


class PriceChannel(models.Model):
    """
    eg. Retail or Matrix
    """
    name = models.CharField(max_length=100)
    
    
class PriceCalculation(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    price_channel = models.ForeignKey(PriceChannel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField(ProductCategory, blank=True)
    product_offerings = models.ManyToManyField(ProductOffering, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    accounts = models.ManyToManyField(CustomerAccount, blank=True)
    stores = models.ManyToManyField(Store, blank=True)

    mode = models.CharField(max_length=200, choices=(('cost plus', 'cost plus'), ('retail minus', 'retail minus'), ('fixed', 'fixed'), ), default='retail minus')
    mode_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    
class Promotion(models.Model):
    code = models.CharField(primary_key=True, max_length=50)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    price_channel = models.ForeignKey(PriceChannel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField(ProductCategory, blank=True)
    product_offerings = models.ManyToManyField(ProductOffering, blank=True)
    customers = models.ManyToManyField(Customer, blank=True)
    stores = models.ManyToManyField(Store, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name

    
class ProductOfferingPrice(models.Model):
    product_offering = models.ForeignKey(ProductOffering, on_delete=models.CASCADE, related_name='product_offering_prices')
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True, related_name='product_offering_prices')
    calculation = models.ForeignKey(PriceCalculation, on_delete=models.CASCADE, null=True, blank=True, related_name='product_offering_prices')

    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, null=True, blank=True, related_name='product_offering_prices')
    quote = models.ForeignKey('order.Quote', on_delete=models.CASCADE, null=True, blank=True, related_name='product_offering_prices')

    #pickslip
    #threshold
    #UOM

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s %s"%( self.product_offering, self.name )
    