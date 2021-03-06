from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.pricing.models import Promotion, ProductOfferingPrice, PriceChannel, PriceCalculation
from retail.pricing.serializers import PromotionSerializer, ProductOfferingPriceSerializer, PriceChannelSerializer, PriceCalculationSerializer


class PriceCalculationViewSet(viewsets.ModelViewSet):
    queryset = PriceCalculation.objects.all()
    serializer_class = PriceCalculationSerializer

    
class PriceChannelViewSet(viewsets.ModelViewSet):
    queryset = PriceChannel.objects.all()
    serializer_class = PriceChannelSerializer

    
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class ProductOfferingPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductOfferingPrice.objects.all()
    serializer_class = ProductOfferingPriceSerializer

    