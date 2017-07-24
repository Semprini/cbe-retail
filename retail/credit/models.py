from django.db import models

from cbe.customer.models import Customer, CustomerAccount
from cbe.party.models import Organisation
from cbe.location.models import AbsoluteLocalLocation
from retail.sale.models import Sale


class CreditProfile(models.Model):
    customer = models.ForeignKey(Customer)
    credit_agency = models.ForeignKey(Organisation,null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    credit_risk_rating = models.IntegerField(null=True, blank=True)
    credit_score = models.IntegerField(null=True, blank=True)
    
    
    
class CreditAlert(models.Model):
    customer = models.ForeignKey(Customer)
    profile = models.ForeignKey(CreditProfile,null=True, blank=True)
    credit_agency = models.ForeignKey(Organisation,null=True, blank=True)

    alert_type = models.CharField(max_length=300, choices = (('risk', 'risk'), ('threshold', 'threshold'),
                           ('breech', 'breech'), ('other', 'other')))
                           
    description = models.TextField(blank=True)
    
    
class CreditBalanceEvent(models.Model):
    customer = models.ForeignKey(Customer)
    account = models.ForeignKey(CustomerAccount)
    location = models.ForeignKey(AbsoluteLocalLocation)
    sale = models.ForeignKey(Sale, null=True, blank=True, related_name='credit_balance_events') #TODO: return or other types
    datetime = models.DateTimeField(auto_now_add=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    