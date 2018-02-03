from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.party.serializers import OrganisationSerializer
from cbe.utils.serializer_fields import TypeField, ExtendedModelSerializerField
from cbe.human_resources.serializers import IdentificationSerializer

from cbe.party.models import Organisation
from retail.loyalty.models import LoyaltyTransaction, LoyaltyScheme
                 
                  
class LoyaltySchemeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = LoyaltyScheme
        fields = ('type', 'url', 'name' )  

        
class LoyaltyTransactionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    scheme = ExtendedModelSerializerField(LoyaltySchemeSerializer(), many=False)
    identification = ExtendedModelSerializerField(IdentificationSerializer(), many=False)
    vendor = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = LoyaltyTransaction
        fields = ('type', 'url', 'created','scheme', 'vendor', 'promotion', 'sale', 'sale_items', 'payment', 'loyalty_amount', 'identification')

        
        