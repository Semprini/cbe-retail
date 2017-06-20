from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.market.models import MarketSegment, MarketStrategy
from retail.market.serializers import MarketSegmentSerializer, MarketStrategySerializer


class MarketSegmentViewSet(viewsets.ModelViewSet):
    queryset = MarketSegment.objects.all()
    serializer_class = MarketSegmentSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    

class MarketStrategyViewSet(viewsets.ModelViewSet):
    queryset = MarketStrategy.objects.all()
    serializer_class = MarketStrategySerializer
    permission_classes = (permissions.DjangoModelPermissions, )    