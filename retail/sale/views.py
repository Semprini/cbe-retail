from rest_framework import permissions, viewsets, status
from rest_framework.decorators import detail_route, list_route, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import BaseParser

from retail.sale.models import Sale, SaleItem, Tender, TenderType, SalesChannel, Purchaser
from retail.sale.serializers import SaleSerializer, SaleItemSerializer, TenderSerializer, TenderTypeSerializer, SalesChannelSerializer, PurchaserSerializer
from retail.sale.utils import ImportDSRLine, ImportDSR

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
        

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    filter_fields = ('channel','store','vendor',)

    @list_route(methods=['post'], parser_classes=(PlainTextParser,))
    def dsr_single(self, request):
        try:
            sale = ImportDSRLine(request.data.decode("utf-8", "ignore"))
            serializer = self.get_serializer(sale)
            return Response(serializer.data)
        except:
            return Response({'Error':'foo'},
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], parser_classes=(PlainTextParser,))
    def dsr(self, request):
        try:
            sale = ImportDSR(request.data.decode("utf-8", "ignore"))
            return Response("Created {} sales".format(sale[5]))
        except:
            return Response({'Error':'foo'},
                            status=status.HTTP_400_BAD_REQUEST)
                            
    
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
    