import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.supply_chain.models import Asns, PoExpectedDeliveryDate, PurchaseOrderAcknowledgementLineItems, PurchaseOrderAcknowledgements, PurchaseOrderLineItems, PurchaseOrders, SchemaVersion, Sscc, SsccAuditCorrectionActions, SsccAuditCorrectionProductItems, SsccAuditCorrectionReversal, SsccAuditCorrections, SsccAuditProductItems, SsccAudits, SsccDelivery, SsccGoodsReceipt, SsccMandatoryAuditControl, SsccProductItems, Synchronisations, SynchronisationsEnd, UnrecognisedSscc
from retail.supply_chain.serializers import AsnsSerializer


class AsnsViewSet(viewsets.ModelViewSet):
    queryset = Asns.objects.all()
    serializer_class = AsnsSerializer


    