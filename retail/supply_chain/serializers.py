from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.supply_chain.models import Asns, PoExpectedDeliveryDate, PurchaseOrderAcknowledgementLineItems, PurchaseOrderAcknowledgements, PurchaseOrderLineItems, PurchaseOrders, SchemaVersion, Sscc, SsccAuditCorrectionActions, SsccAuditCorrectionProductItems, SsccAuditCorrectionReversal, SsccAuditCorrections, SsccAuditProductItems, SsccAudits, SsccDelivery, SsccGoodsReceipt, SsccMandatoryAuditControl, SsccProductItems, Synchronisations, SynchronisationsEnd, UnrecognisedSscc


class AsnsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Asns
        fields = ('type', 'url', 'asn_reference', 'message_date_time', 'message_received_date_time', 
                    'despatch_date_time', 'shipment_due_date_time','final_shipment_flag','purchase_order_reference',
                    'mitre_10_supplier_code','mitre_10_buyer_store_code','mitre_10_delivery_store_code' )


