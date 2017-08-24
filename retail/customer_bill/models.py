from django.db import models

from cbe.location.models import Location
from cbe.party.models import Organisation
from cbe.customer.models import Customer, CustomerAccount

from retail.sale.models import Sale


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
    organisation = models.ForeignKey( Organisation, null=True, blank=True )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.account, self.name )
    
    
class CustomerBill(models.Model):
    account = models.ForeignKey( CustomerAccount )
    specification = models.ForeignKey( CustomerBillSpecification )

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
    bill = models.ForeignKey( CustomerBill )
    
    ITEM_TYPE_CHOICES = ( ('account', 'account'), ('subscription', 'subscription'), ('service', 'service'), ('rebate','rebate'), ('allocation', 'allocation'), ('adjustment', 'adjustment'), ('dispute', 'dispute'), )
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
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s:%s" %(self.bill, self.item_type )

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

#account charge
#subscription charge
#service charge

