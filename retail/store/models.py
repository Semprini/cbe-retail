from django.db import models

from cbe.location.models import Location
from cbe.party.models import Organisation, PartyRole

class Store(PartyRole):
    code = models.CharField(max_length=200, blank=True, null=True)

    location = models.ForeignKey(Location, blank=True, null=True)
    
    class Meta:
        ordering = ['id']

        
    def __str__(self):
        return "%s" %(self.name )    
        
        
    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Store"          
        super(Store, self).save(*args, **kwargs)        