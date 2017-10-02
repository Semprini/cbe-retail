from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake, ProductAssociation, SupplierProduct, ProductSpecification
from retail.product.serializers import ProductSerializer, ProductOfferingSerializer, ProductCategorySerializer, ProductStockSerializer, ProductStockTakeSerializer, ProductAssociationSerializer, SupplierProductSerializer, ProductSpecificationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
class ProductOfferingViewSet(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    filter_fields = ('status',)

    
class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = ProductStock.objects.all()
    serializer_class = ProductStockSerializer
    filter_fields = ('store',)

    
class ProductStockTakeViewSet(viewsets.ModelViewSet):
    queryset = ProductStockTake.objects.all()
    serializer_class = ProductStockTakeSerializer
    filter_fields = ('store',)
    
    
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    
class ProductAssociationViewSet(viewsets.ModelViewSet):
    queryset = ProductAssociation.objects.all()
    serializer_class = ProductAssociationSerializer
    filter_fields = ('rank',)

    
class SupplierProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierProduct.objects.all()
    serializer_class = SupplierProductSerializer

    
class ProductSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    
    