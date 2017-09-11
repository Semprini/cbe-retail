from django.db import models

from cbe.party.models import Organisation, Individual
from cbe.human_resources.models import Identification, IdentificationType
from retail.sale.models import Sale, SaleItem, Promotion


class LoyaltyScheme( models.Model ):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name,)

        
class LoyaltyTransaction( models.Model ):
    created = models.DateTimeField(auto_now_add=True)
    
    scheme = models.ForeignKey(LoyaltyScheme)
    vendor = models.ForeignKey(Organisation)
    identification = models.ForeignKey(Identification)
    
    sale = models.ForeignKey(Sale, db_index=True, related_name='loyalty_transactions', null=True,blank=True)
    items = models.ManyToManyField(SaleItem, blank=True)
    #payment = models.ForeignKey(Payment, db_index=True, related_name='loyalty_transactions', null=True,blank=True)
    promotion = models.ForeignKey(Promotion, null=True,blank=True)
    
    loyalty_amount = models.DecimalField(max_digits=10, decimal_places=2)

    