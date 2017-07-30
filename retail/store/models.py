from django.db import models

from cbe.location.models import Location
from cbe.party.models import Organisation

class Store(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, blank=True, null=True)

    location = models.ForeignKey(Location, blank=True, null=True)
    owner = models.ForeignKey(Organisation, blank=True, null=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s" %(self.name )    
        
        