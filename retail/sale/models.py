from django.utils.timezone import now
from django.db import models

from cbe.party.models import Organisation, PartyRole
from cbe.customer.models import Customer, CustomerAccount
from cbe.resource.models import PhysicalResource
from cbe.human_resources.models import Staff, Identification
from cbe.credit.models import Credit, CreditBalanceEvent

from retail.store.models import Store
from retail.product.models import ProductOffering, Product
from retail.pricing.models import PriceChannel, PriceCalculation, Promotion, ProductOfferingPrice
from retail.job_management.models import Job


class Purchaser(PartyRole):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s"%(self.party)

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Purchaser"          
        super(Purchaser, self).save(*args, **kwargs)
        

class SalesChannel(models.Model):
    name =  models.CharField(max_length=100 )

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s"%(self.name)


class Sale(models.Model):
    channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    
    datetime = models.DateTimeField(default=now)
    status = models.CharField(max_length=200, choices=(('basket', 'basket'), ('complete', 'complete')), default='complete')
    docket_number = models.CharField(max_length=50, null=True,blank=True )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount_excl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    purchaser = models.ForeignKey(Purchaser, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    identification = models.ForeignKey(Identification, on_delete=models.CASCADE, null=True,blank=True )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_index=True, null=True,blank=True)

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True,blank=True)
    till = models.ForeignKey(PhysicalResource, on_delete=models.CASCADE, db_index=True, null=True,blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_index=True, null=True,blank=True)

    credit_balance_events = models.ManyToManyField(CreditBalanceEvent, blank=True)

    class Meta:
        ordering = ['-datetime']
        
    def __str__(self):
        return "%s|%s|%d"%(self.store,self.datetime,self.total_amount)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, db_index=True, related_name='sale_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, )
    product_offering = models.ForeignKey(ProductOffering, on_delete=models.CASCADE, db_index=True, )

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True,blank=True)
    price_channel = models.ForeignKey(PriceChannel, on_delete=models.CASCADE, null=True,blank=True)
    price_calculation = models.ForeignKey(PriceCalculation, on_delete=models.CASCADE, null=True,blank=True)

    product_offering_price = models.ForeignKey('pricing.ProductOfferingPrice', on_delete=models.CASCADE, null=True, blank=True )
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('square metre', 'square metre'), ('lineal metre', 'metre')), default='each')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return "%s"%self.product_offering


class TenderType(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Tender(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, db_index=True, related_name='tenders')
    tender_type = models.ForeignKey(TenderType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s %s"%(self.sale, self.tender_type)



    
