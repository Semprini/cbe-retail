from django.db import models

from cbe.human_resources.models import Identification, IdentificationType
from retail.sale.models import Sale, SaleItem, Promotion


class LoyaltyScheme( models.Model ):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name,)

        
class LoyaltyCardType( IdentificationType ):
    pass
    
    
class LoyaltyCard( Identification ):
    pass
    
    
class LoyaltyTransaction( models.Model ):
    sale = models.ForeignKey(Sale, db_index=True, related_name='loyalty_transactions', on_delete=models.CASCADE)
    items = models.ManyToManyField(SaleItem, blank=True)
    promotion = models.ForeignKey(Promotion, null=True,blank=True)
    scheme = models.ForeignKey(LoyaltyScheme, null=True,blank=True)
    
    loyalty_amount = models.DecimalField(max_digits=10, decimal_places=2)

    