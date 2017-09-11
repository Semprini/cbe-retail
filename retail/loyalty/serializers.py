from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.party.serializers import OrganisationSerializer
from cbe.utils.serializer_fields import TypeField, ExtendedSerializerField
from retail.loyalty.models import LoyaltyTransaction, LoyaltyScheme
from cbe.human_resources.serializers import IdentificationSerializer
                 
                  
class LoyaltySchemeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = LoyaltyScheme
        fields = ('type', 'url', 'name' )  

        
class LoyaltyTransactionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    scheme = ExtendedSerializerField(LoyaltySchemeSerializer(), many=False)
    identification = ExtendedSerializerField(IdentificationSerializer(), many=False)

    class Meta:
        model = LoyaltyTransaction
        fields = ('type', 'url', 'created','scheme', 'vendor', 'promotion', 'sale', 'items', 'loyalty_amount', 'identification')

        
        