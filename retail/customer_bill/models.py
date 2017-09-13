from django.db import models

from cbe.location.models import Location
from cbe.customer.models import Customer, CustomerAccount
from cbe.party.models import Organisation

from retail.sale.models import Sale
from retail.job_management.models import Job


class CustomerBillingCycle(models.Model):
    account = models.ForeignKey( CustomerAccount )

    name = models.CharField(max_length=200)

    billing_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    payment_due = models.DateField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.account, self.name )
    
    
class CustomerBillSpecification(models.Model):
    name = models.CharField(max_length=200)
    account = models.ForeignKey( CustomerAccount )
    
    billing_cycle = models.ForeignKey( CustomerBillingCycle )
    location = models.ForeignKey( Location, null=True, blank=True )
    customer = models.ForeignKey( Customer, null=True, blank=True )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.account, self.name )
    
    
class CustomerBill(models.Model):
    account = models.ForeignKey( CustomerAccount )
    specification = models.ForeignKey( CustomerBillSpecification )
    customer = models.ForeignKey( Customer )

    number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    period_from = models.DateField()
    period_to = models.DateField()
    
    BILL_STATUS_CHOICES = ( ('inactive', 'inactive'), ('active', 'active'), ('due', 'due'), ('disputed', 'disputed'), ('closed','closed') )
    status = models.CharField(max_length=100, choices=BILL_STATUS_CHOICES)

    amount = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    discounted = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    adjusted = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    rebated = models.DecimalField(default = 0, max_digits=10, decimal_places=2)

    disputed = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    allocated = models.DecimalField(default = 0, max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.account, self.number )
    
    
class CustomerBillItem(models.Model):
    bill = models.ForeignKey( CustomerBill, related_name="%(class)ss" )
    
    ITEM_TYPE_CHOICES = ( ('account', 'account'), ('job', 'job'), ('subscription', 'subscription'), ('service', 'service'), ('rebate','rebate'), ('allocation', 'allocation'), ('adjustment', 'adjustment'), ('dispute', 'dispute'), )
    item_type = models.CharField(max_length=100, choices=ITEM_TYPE_CHOICES)

    amount = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    discounted = models.DecimalField(default = 0, max_digits=10, decimal_places=2)

    sale_events = models.ManyToManyField(Sale, blank=True)
    
    class Meta:
        ordering = ['id']

    class Meta:
        abstract = True    
    
    
class AccountBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )
    
class JobBillItem(CustomerBillItem):
    job = models.ForeignKey( Job )
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.job )

class SubscriptionBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

class ServiceBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

class RebateBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

class AllocationBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

class AdjustmentBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

class DisputeBillItem(CustomerBillItem):
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

        
class ServiceCharge(models.Model):
    bill = models.ForeignKey( CustomerBill, related_name="%(class)ss" )
    service_bill_item = models.ForeignKey( ServiceBillItem, related_name="%(class)ss", null=True, blank=True )
    
    sales = models.ManyToManyField(Sale, blank=True)
    home_store = models.ForeignKey( Organisation, null=True, blank=True, related_name="home_service_charges" )
    satellite_store = models.ForeignKey( Organisation, null=True, blank=True, related_name="satellite_service_charges" )

    total_margin = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    home_margin = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    satellite_margin = models.DecimalField(default = 0, max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']
    