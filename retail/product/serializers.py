from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.product.models import Product, ProductOffering, ProductCategory, ProductStockLevel, ProductAssociation


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
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name', 'description', 'unit_of_measure', 'sku', 'barcode', 'bundle', 'categories', 'cross_sell_products',)


class ProductOfferingSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    product = ProductSerializer()
    
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
        fields = ('type', 'url', 'valid_from', 'valid_to', 'parent', 'level', 'name', 'description', )


