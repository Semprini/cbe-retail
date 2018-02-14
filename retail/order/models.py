from django.utils.timezone import now
from django.db import models

from cbe.party.models import Organisation
from cbe.location.models import Location
from cbe.customer.models import Customer, CustomerAccount

from retail.store.models import Store
from retail.sale.models import SalesChannel
from retail.product.models import ProductOffering, Product
from retail.pricing.models import PriceChannel, PriceCalculation, Promotion


class Order(models.Model):
    channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    seller = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=now)
    order_type = models.CharField(max_length=200, choices=(('order', 'order'), ('quote', 'quote'), ('estimate', 'estimate')), default='order')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_excl = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True, null=True,blank=True)

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True,blank=True)

    price_channel = models.ForeignKey(PriceChannel, on_delete=models.CASCADE, null=True,blank=True)
    price_calculation = models.ForeignKey(PriceCalculation, on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s|%s|%d"%(self.location,self.datetime,self.total_amount)

    def save(self, *args, **kwargs):
        self.order_type = "Order"
        super(Order, self).save(*args, **kwargs)        
        
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, db_index=True, related_name='order_items', on_delete=models.CASCADE)
    #product = models.ForeignKey(product, db_index=True, )
    product_offering = models.ForeignKey(ProductOffering, on_delete=models.CASCADE, db_index=True, )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('metre', 'metre')), default='each')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return "%s"%self.product
        
    
class Quote(Order):
    def save(self, *args, **kwargs):
        self.order_type = "Quote"
        super(Quote, self).save(*args, **kwargs)        

    
class Estimate(Order):
    def save(self, *args, **kwargs):
        self.order_type = "Estimate"
        super(Estimate, self).save(*args, **kwargs)        

    
