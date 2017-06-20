from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStockLevel
from retail.product.serializers import ProductSerializer, ProductOfferingSerializer, ProductCategorySerializer, ProductStockLevelSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductOfferingViewSet(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductStockLevelViewSet(viewsets.ModelViewSet):
    queryset = ProductStockLevel.objects.all()
    serializer_class = ProductStockLevelSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
    