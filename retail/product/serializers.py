from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializers import LimitDepthMixin
from cbe.utils.serializer_fields import TypeField
from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake, ProductAssociation, SupplierProduct, ProductSpecification


class ProductAssociationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductAssociation
        fields = ('type', 'url', 'valid_from', 'valid_to', 'from_product', 'to_product', 'association_type', 'rank',)

        
class ProductSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #product_associations = serializers.HyperlinkedIdentityField(many=True, view_name='productassociation-detail')
    #product_associations = ProductAssociationSerializer(many=True)
    cross_sell_products = serializers.HyperlinkedIdentityField(many=True, view_name='product-detail')
    
    class Meta:
        model = Product
        fields = ('type', 'url', 'code', 'name', 'description',  'bundle', 'categories', 'cross_sell_products', 'product_offerings', 'supplier_products', 'specifiactions')


class ProductOfferingSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    product = ProductSerializer()
    
    class Meta:
        model = ProductOffering
        fields = ('type', 'url', 'valid_from', 'valid_to', 'sku', 'product', 'specification',
                    'department', 'sub_department', 'fineline', 'channels', 'segments', 'strategies', 
                    'unit_of_measure', 'retail_price', 'average_cost_price', 'product_offering_prices' )

                  
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
        fields = ('type', 'url', 'valid_from', 'valid_to', 'id', 'parent', 'level', 'name', 'description', )


class SupplierProductSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SupplierProduct
        fields = ( 'type', 'url', 'supplier_sku', 'barcode', 'product', 'supplier', 'buyer', 'unit_of_measure','cost_price','reccomended_retail_price' )

        
class ProductSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ProductSpecification
        fields = ( 'type', 'url', 'colour_name', 'colour_value', 'size_name', 'size_value')

        