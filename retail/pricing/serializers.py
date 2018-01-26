from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.pricing.models import Promotion, ProductOfferingPrice, PriceChannel, PriceCalculation


class PriceChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    class Meta:
        model = PriceChannel
        fields = ('type', 'url', 'name')

        
class PriceCalculationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    class Meta:
        model = PriceCalculation
        fields = ('type', 'url', 'valid_from', 'valid_to', 
                    'price_channel', 'name', 'description', 
                    'categories', 'product_offerings', 'customers', 'accounts', 'stores',
                    'mode', 'mode_amount')
        
        
class ProductOfferingPriceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductOfferingPrice
        fields = ('type', 'url', 'product_offering', 'promotion', 'account', 'valid_from', 'valid_to', 'name',
                  'description', 'categories')

                  
class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Promotion
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', 'categories', 'product_offerings','product_offering_prices','customers')
