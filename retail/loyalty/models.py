from django.db import models

from cbe.party.models import Organisation, Individual
from cbe.human_resources.models import Identification, IdentificationType
from cbe.accounts_receivable.models import CustomerPayment
from retail.sale.models import Sale, SaleItem, Promotion


class LoyaltyScheme( models.Model ):
    name = models.CharField(max_length=200)
    loyalty_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return "{}".format(self.name,)

        
class LoyaltyTransaction( models.Model ):
    created = models.DateTimeField(auto_now_add=True)
    
    scheme = models.ForeignKey(LoyaltyScheme, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    identification = models.ForeignKey(Identification, on_delete=models.CASCADE)
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, db_index=True, related_name='loyalty_transactions', null=True,blank=True)
    sale_items = models.ManyToManyField(SaleItem, blank=True)
    payment = models.ForeignKey(CustomerPayment, on_delete=models.CASCADE, db_index=True, related_name='loyalty_transactions', null=True,blank=True)
    
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True,blank=True)
    
    loyalty_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']    
    