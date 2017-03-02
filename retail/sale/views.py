import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.sale.models import Sale, SaleItem, Tender, TenderType, LoyaltyTransaction
from retail.sale.serializers import SaleSerializer, SaleItemSerializer, TenderSerializer, TenderTypeSerializer, LoyaltyTransactionSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
    filter_fields = ('store','datetime',)
    search_fields = ('customer', 'promotion')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,)
    

        
class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

class TenderTypeViewSet(viewsets.ModelViewSet):
    queryset = TenderType.objects.all()
    serializer_class = TenderTypeSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

class LoyaltyTransactionViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
    