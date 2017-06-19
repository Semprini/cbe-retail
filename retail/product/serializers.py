from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.product.models import ProductOffering, ProductCategory, Promotion, ProductOfferingPrice


class ProductOfferingSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    #prices = serializers.ManyHyperlinkedRelatedField(
    #    source='productofferingprice_set',
    #    view_name='productofferingprice-detail' 
    #)
    
    class Meta:
        model = ProductOffering
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', 'sku', 'categories', 'channels', 'segments', 'strategies', 'retail_price', 'product_offering_prices', 'supplier','buyer')


class ProductOfferingPriceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductOfferingPrice
        fields = ('type', 'url', 'product_offering', 'promotion', 'valid_from', 'valid_to', 'name',
                  'description', 'categories', 'amount')

                  
class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductCategory
        fields = ('type', 'url', 'valid_from', 'valid_to', 'parent', 'level', 'name',
                  'description', )


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Promotion
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', 'categories', 'products','customers')
