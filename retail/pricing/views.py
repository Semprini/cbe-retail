from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.pricing.models import Promotion, ProductOfferingPrice
from retail.pricing.serializers import PromotionSerializer, ProductOfferingPriceSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class ProductOfferingPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductOfferingPrice.objects.all()
    serializer_class = ProductOfferingPriceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

    