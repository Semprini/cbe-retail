from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from cbe.location.models import Location, GeographicArea
from cbe.party.models import Organisation, PartyRole
from cbe.physical_object.models import Structure

class Store(PartyRole):
    enterprise_id = models.IntegerField(unique=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    identifiers = GenericRelation('human_resources.Identification', object_id_field="party_role_object_id", content_type_field='party_role_content_type', related_query_name='store')    
    
    store_type = models.CharField( max_length=100, null=True, blank=True, choices=(('mitre 10','mitre 10'),('mega','mega'),('hammer','hammer'),('trade','trade')) )
    store_class = models.CharField( max_length=100, null=True, blank=True, choices=(('mega-1','mega-1'),('mega-2','mega-2'),('mega-3','mega-3'),('mega-r','mega-r'),('mitre10-small','mitre10-small'),('mitre10-medium','mitre10-medium'),('mitre10-large','mitre10-large'),('trade','trade')) )

    opening_date = models.DateField(blank=True, null=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    
    trade_area = models.ForeignKey(GeographicArea, on_delete=models.CASCADE, related_name='store_trade_areas', blank=True, null=True)
    retail_area = models.ForeignKey(GeographicArea, on_delete=models.CASCADE, related_name='store_retail_areas', blank=True, null=True)
    national_area = models.ForeignKey(GeographicArea, on_delete=models.CASCADE, related_name='store_national_areas', blank=True, null=True)
    
    buildings = models.ManyToManyField(Structure, related_name='store')
    
    class Meta:
        ordering = ['id']

        
    def __str__(self):
        return "%s" %(self.name )    
        
        
    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Store"          
        super(Store, self).save(*args, **kwargs)        