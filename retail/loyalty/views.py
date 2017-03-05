import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets

from retail.loyalty.models import LoyaltyTransaction, LoyaltyCard, LoyaltyScheme, LoyaltyCardType
from retail.loyalty.serializers import LoyaltyTransactionSerializer, LoyaltyCardSerializer, LoyaltySchemeSerializer, LoyaltyCardTypeSerializer

class LoyaltyTransactionViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
    
    
class LoyaltySchemeViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyScheme.objects.all()
    serializer_class = LoyaltySchemeSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )    
    
    
class LoyaltyCardTypeViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyCardType.objects.all()
    serializer_class = LoyaltyCardTypeSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )    

    
class LoyaltyCardViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyCard.objects.all()
    serializer_class = LoyaltyCardSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )    
    