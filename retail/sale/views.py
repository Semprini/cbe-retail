from rest_framework import permissions, viewsets

from retail.sale.models import Sale, SaleItem, Tender, TenderType, SalesChannel, Purchaser
from retail.sale.serializers import SaleSerializer, SaleItemSerializer, TenderSerializer, TenderTypeSerializer, SalesChannelSerializer, PurchaserSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    filter_fields = ('channel','store','vendor',)

    
class SalesChannelViewSet(viewsets.ModelViewSet):
    queryset = SalesChannel.objects.all()
    serializer_class = SalesChannelSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

        
class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

class TenderTypeViewSet(viewsets.ModelViewSet):
    queryset = TenderType.objects.all()
    serializer_class = TenderTypeSerializer
    permission_classes = (permissions.DjangoModelPermissions, )

    
class PurchaserViewSet(viewsets.ModelViewSet):
    queryset = Purchaser.objects.all()
    serializer_class = PurchaserSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    