from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.product.models import Product, ProductOffering, ProductCategory, ProductStockLevel


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Product
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name', 'description', 'unit_of_measure', 'sku', 'bundle', 'categories')

        
class ProductOfferingSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    #prices = serializers.ManyHyperlinkedRelatedField(
    #    source='productofferingprice_set',
    #    view_name='productofferingprice-detail' 
    #)
    
    class Meta:
        model = ProductOffering
        fields = ('type', 'url', 'valid_from', 'valid_to', 'product', 'channels', 'segments', 'strategies', 'supplier_code', 'retail_price', 'product_offering_prices', 'supplier','buyer')

                  
class ProductStockLevelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductStockLevel
        fields = ('type', 'url', 'datetime', 'store', 'product','location','amount','average')
    
    
class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductCategory
        fields = ('type', 'url', 'valid_from', 'valid_to', 'parent', 'level', 'name',
                  'description', )


