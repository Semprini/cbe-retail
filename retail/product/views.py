from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake, ProductAssociation, SupplierProduct
from retail.product.serializers import ProductSerializer, ProductOfferingSerializer, ProductCategorySerializer, ProductStockSerializer, ProductStockTakeSerializer, ProductAssociationSerializer, SupplierProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductOfferingViewSet(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = ProductStock.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductStockTakeViewSet(viewsets.ModelViewSet):
    queryset = ProductStockTake.objects.all()
    serializer_class = ProductStockTakeSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
    
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductAssociationViewSet(viewsets.ModelViewSet):
    queryset = ProductAssociation.objects.all()
    serializer_class = ProductAssociationSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class SupplierProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierProduct.objects.all()
    serializer_class = SupplierProductSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
    