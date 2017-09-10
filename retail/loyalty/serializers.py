from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.loyalty.models import LoyaltyTransaction, LoyaltyScheme
from cbe.human_resources.serializers import IdentificationSerializer
                 
                  
class LoyaltySchemeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = LoyaltyScheme
        fields = ('type', 'url', 'name' )  

        
class LoyaltyTransactionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    scheme = LoyaltySchemeSerializer()
    identification = IdentificationSerializer()

    class Meta:
        model = LoyaltyTransaction
        fields = ('type', 'url', 'created','scheme', 'vendor', 'promotion', 'sale', 'items', 'loyalty_amount', 'identification')

        
    def get_validation_exclusions(self):
        exclusions = super(LoyaltyTransactionSerializer, self).get_validation_exclusions()
        return exclusions + ['scheme', 'identification']

        
    def create(self, validated_data):
        scheme_data = validated_data.pop('scheme')
        identification_data = validated_data.pop('identification')
        loyalty = LoyaltyTransaction.objects.create(**validated_data)    
        return loyalty


    def update(self, instance, validated_data):
        scheme_data = validated_data.pop('scheme')
        identification_data = validated_data.pop('identification')
        
        for key, value in validated_data.items():
            setattr( instance, key, value )

        instance.save()
        return instance
        
        