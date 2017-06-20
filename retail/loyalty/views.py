import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets

from retail.loyalty.models import LoyaltyTransaction, LoyaltyScheme
from retail.loyalty.serializers import LoyaltyTransactionSerializer, LoyaltySchemeSerializer

class LoyaltyTransactionViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
    
class LoyaltySchemeViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyScheme.objects.all()
    serializer_class = LoyaltySchemeSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    
    
    
