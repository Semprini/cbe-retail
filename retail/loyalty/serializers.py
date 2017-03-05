from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.party.serializers import PartyRelatedField
from retail.loyalty.models import LoyaltyTransaction, LoyaltyCard, LoyaltyScheme, LoyaltyCardType

                 
                  
class LoyaltyTransactionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = LoyaltyTransaction
        fields = ('type', 'url', 'scheme', 'promotion', 'sale', 'items', 'loyalty_amount', )                  
        

class LoyaltySchemeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = LoyaltyScheme
        fields = ('type', 'url', 'name' )  

        
class LoyaltyCardTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = LoyaltyCardType
        fields = ('type', 'url', 'name' )  
        
        
class LoyaltyCardSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = PartyRelatedField()
    
    class Meta:
        model = LoyaltyCard
        fields = ('type', 'url', 'identification_type', 'number', 'party' )                          