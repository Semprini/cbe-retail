from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.pricing.models import Promotion, ProductOfferingPrice


class ProductOfferingPriceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductOfferingPrice
        fields = ('type', 'url', 'product_offering', 'promotion', 'valid_from', 'valid_to', 'name',
                  'description', 'categories', 'amount')

                  
class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Promotion
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', 'categories', 'products','customers')
