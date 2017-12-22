from django.db import models

from cbe.location.models import Location
from cbe.party.models import Organisation, PartyRole

class Store(PartyRole):
    code = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    store_class = models.CharField( max_length=100, null=True, blank=True, choices=(('mitre 10','mitre 10'),('mega','mega'),('hammer','hammer')) )

    opening_date = models.DateField(blank=True, null=True)
    
    location = models.ForeignKey(Location, blank=True, null=True)
    
    class Meta:
        ordering = ['id']

        
    def __str__(self):
        return "%s" %(self.name )    
        
        
    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Store"          
        super(Store, self).save(*args, **kwargs)        