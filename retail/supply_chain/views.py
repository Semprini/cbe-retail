import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.supply_chain.models import Asns, PoExpectedDeliveryDate, PurchaseOrderAcknowledgementLineItems, PurchaseOrderAcknowledgements
from retail.supply_chain.models import PurchaseOrderLineItems, PurchaseOrders, SchemaVersion, Sscc, SsccAuditCorrectionActions
from retail.supply_chain.models import SsccAuditCorrectionProductItems, SsccAuditCorrectionReversal, SsccAuditCorrections
from retail.supply_chain.models import SsccAuditProductItems, SsccAudits, SsccDelivery, SsccGoodsReceipt, SsccMandatoryAuditControl
from retail.supply_chain.models import SsccProductItems, Synchronisations, SynchronisationsEnd, UnrecognisedSscc
from retail.supply_chain.serializers import AsnsSerializer, PoExpectedDeliveryDateSerializer, PurchaseOrderAcknowledgementLineItemsSerializer
from retail.supply_chain.serializers import PurchaseOrderAcknowledgementsSerializer, PurchaseOrderLineItemsSerializer, PurchaseOrdersSerializer
from retail.supply_chain.serializers import SsccAuditCorrectionsSerializer, SsccAuditProductItemsSerializer
from retail.supply_chain.serializers import SchemaVersionSerializer, SsccSerializer, SsccAuditCorrectionActionsSerializer, SsccAuditCorrectionProductItemsSerializer
from retail.supply_chain.serializers import SsccAuditCorrectionReversalSerializer, SsccAuditsSerializer, SsccDeliverySerializer, SsccGoodsReceiptSerializer, SsccMandatoryAuditControlSerializer
from retail.supply_chain.serializers import SsccProductItemsSerializer, SynchronisationsSerializer, SynchronisationsEndSerializer, UnrecognisedSsccSerializer


class AsnsViewSet(viewsets.ModelViewSet):
    queryset = Asns.objects.all()
    serializer_class = AsnsSerializer

class PoExpectedDeliveryDateViewSet(viewsets.ModelViewSet):
    queryset = PoExpectedDeliveryDate.objects.all()
    serializer_class = PoExpectedDeliveryDateSerializer

class PurchaseOrderAcknowledgementLineItemsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderAcknowledgementLineItems.objects.all()
    serializer_class = PurchaseOrderAcknowledgementLineItemsSerializer

class PurchaseOrderAcknowledgementsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderAcknowledgements.objects.all()
    serializer_class = PurchaseOrderAcknowledgementsSerializer

class PurchaseOrderLineItemsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderLineItems.objects.all()
    serializer_class = PurchaseOrderLineItemsSerializer

class PurchaseOrdersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrdersSerializer
    
class SchemaVersionViewSet(viewsets.ModelViewSet):
    queryset = SchemaVersion.objects.all()
    serializer_class = SchemaVersionSerializer    

class SsccViewSet(viewsets.ModelViewSet):
    queryset = Sscc.objects.all()
    serializer_class = SsccSerializer    

class SsccAuditCorrectionActionsViewSet(viewsets.ModelViewSet):
    queryset = SsccAuditCorrectionActions.objects.all()
    serializer_class = SsccAuditCorrectionActionsSerializer    

class SsccAuditCorrectionProductItemsViewSet(viewsets.ModelViewSet):
    queryset = SsccAuditCorrectionProductItems.objects.all()
    serializer_class = SsccAuditCorrectionProductItemsSerializer    

class SsccAuditCorrectionReversalViewSet(viewsets.ModelViewSet):
    queryset = SsccAuditCorrectionReversal.objects.all()
    serializer_class = SsccAuditCorrectionReversalSerializer    

class SsccAuditCorrectionsViewSet(viewsets.ModelViewSet):
    queryset = SsccAuditCorrections.objects.all()
    serializer_class = SsccAuditCorrectionsSerializer    

class SsccAuditProductItemsViewSet(viewsets.ModelViewSet):
    queryset = SsccAuditProductItems.objects.all()
    serializer_class = SsccAuditProductItemsSerializer    

class SsccAuditsViewSet(viewsets.ModelViewSet):
    queryset = SsccAudits.objects.all()
    serializer_class = SsccAuditsSerializer    

class SsccDeliveryViewSet(viewsets.ModelViewSet):
    queryset = SsccDelivery.objects.all()
    serializer_class = SsccDeliverySerializer    

class SsccGoodsReceiptViewSet(viewsets.ModelViewSet):
    queryset = SsccGoodsReceipt.objects.all()
    serializer_class = SsccGoodsReceiptSerializer    

class SsccMandatoryAuditControlViewSet(viewsets.ModelViewSet):
    queryset = SsccMandatoryAuditControl.objects.all()
    serializer_class = SsccMandatoryAuditControlSerializer    

class SsccProductItemsViewSet(viewsets.ModelViewSet):
    queryset = SsccProductItems.objects.all()
    serializer_class = SsccProductItemsSerializer    

class SynchronisationsViewSet(viewsets.ModelViewSet):
    queryset = Synchronisations.objects.all()
    serializer_class = SynchronisationsSerializer    

class SynchronisationsEndViewSet(viewsets.ModelViewSet):
    queryset = SynchronisationsEnd.objects.all()
    serializer_class = SynchronisationsEndSerializer    

class UnrecognisedSsccViewSet(viewsets.ModelViewSet):
    queryset = UnrecognisedSscc.objects.all()
    serializer_class = UnrecognisedSsccSerializer    

