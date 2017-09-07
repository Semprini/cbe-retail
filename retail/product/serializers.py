from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake, ProductAssociation


class ProductAssociationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductAssociation
        fields = ('type', 'url', 'valid_from', 'valid_to', 'from_product', 'to_product', 'association_type', 'rank',)

        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #product_associations = serializers.HyperlinkedIdentityField(many=True, view_name='productassociation-detail')
    #product_associations = ProductAssociationSerializer(many=True)
    cross_sell_products = serializers.HyperlinkedIdentityField(many=True, view_name='product-detail')
    
    class Meta:
        model = Product
        fields = ('type', 'url', 'code', 'name', 'description',  'bundle', 'categories', 'cross_sell_products','product_offerings')


class ProductOfferingSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    product = ProductSerializer()
    
    class Meta:
        model = ProductOffering
        fields = ('type', 'url', 'valid_from', 'valid_to', 'sku', 'product', 'channels', 'segments', 'strategies', 'unit_of_measure', 'retail_price', 'product_offering_prices' )

                  
class ProductStockSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductStock
        fields = ('type', 'url', 'store', 'product','location','unit_of_measure','amount','average', 'reorder_minimum', 'product_stock_takes')
    
    
class ProductStockTakeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductStockTake
        fields = ('type', 'url', 'datetime', 'store', 'product_stock','location','staff','unit_of_measure','amount')


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductCategory
        fields = ('type', 'url', 'valid_from', 'valid_to', 'parent', 'level', 'name', 'description', )


