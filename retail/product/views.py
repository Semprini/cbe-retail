from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.product.models import ProductOffering, ProductCategory, Promotion, ProductOfferingPrice, ProductStockLevel
from retail.product.serializers import ProductOfferingSerializer, ProductCategorySerializer, PromotionSerializer, ProductOfferingPriceSerializer, ProductStockLevelSerializer


class ProductOfferingViewSet(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    
class ProductStockLevelViewSet(viewsets.ModelViewSet):
    queryset = ProductStockLevel.objects.all()
    serializer_class = ProductStockLevelSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    
class ProductOfferingPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductOfferingPrice.objects.all()
    serializer_class = ProductOfferingPriceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    