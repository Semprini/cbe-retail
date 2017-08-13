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


class PoExpectedDeliveryDateSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PoExpectedDeliveryDate
        fields = ('type', 'url', 'purchase_order_reference', 'expected_delivery_date', 'mitre_10_supplier_code', 
                    'message_received_date_time', 'source_record_table', 'source_record_id', 'mitre_10_delivery_store_code' )
                    

class PurchaseOrderAcknowledgementLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PurchaseOrderAcknowledgementLineItems
        fields = ('type', 'url', 'item_barcode', 'mitre_10_item_code', 'supplier_item_code', 
                    'purchase_order_acknowledgement', 'item_description', 'quantity', 'unit',
                    'unit_price','notification_code', 'notification_description',)

                    
class PurchaseOrderAcknowledgementsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PurchaseOrderAcknowledgements
        fields = ('type', 'url', 'poa_reference', 'message_date_time', 'message_received_date_time', 
                    'delivery_date_time_requested', 'delivery_date_time_estimated', 'purchase_order_reference', 'mitre_10_supplier_code',
                    'mitre_10_buyer_store_code','mitre_10_delivery_store_code', 'message_function_code', 'message_function_description', 'latest_flag')

class PurchaseOrderLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PurchaseOrderLineItems
        fields = ('type', 'url', 'purchase_order', 'item_barcode', 'mitre_10_item_code', 
                    'supplier_item_code', 'item_description', 'quantity', 'unit',
                    'unit_price', 'conversion_factor', )

                    
class PurchaseOrdersSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PurchaseOrders
        fields = ('type', 'url', 'purchase_order_reference', 'mitre_10_supplier_code', 'mitre_10_buyer_store_code', 
                    'mitre_10_delivery_store_code', 'purchase_order_date', 'despatched_date_time', 'delivery_due_date',
                    'latest_flag', )

class SchemaVersionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SchemaVersion
        fields = ('type', 'url', 'installed_rank', 'version', 'description', 
                    'type', 'script', 'checksum', 'installed_by',
                    'installed_on', 'execution_time','success' )
                    
class SsccSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Sscc
        fields = ('type', 'url', 'asn', 'sscc_barcode', 'package_type', 
                    'parent_sscc_barcode', 'height_mm', 'width_mm', 'weight_kilos',
                    'length_mm', )

                    
class SsccAuditCorrectionActionsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAuditCorrectionActions
        fields = ('type', 'url', 'audit_correction_action_type', 'audit_correction_reference', 'goods_receipt_reference_date', 
                    'sscc_audit_correction', )                    
                    
class SsccAuditCorrectionProductItemsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAuditCorrectionProductItems
        fields = ('type', 'url', 'mitre_10_item_code', 'quantity', 'sscc_audit_correction_action', )   
        
        
class SsccAuditCorrectionReversalSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAuditCorrectionReversal
        fields = ('type', 'url', 'submitted_by', 'submitted_date_time', 'sscc_audit_correction', )   

        
class SsccAuditCorrectionsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAuditCorrections
        fields = ('type', 'url', 'sscc_audits', )   

        
class SsccAuditProductItemsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAuditProductItems
        fields = ('type', 'url', 'sscc_audit', 'item_barcode','mitre10_item_code', 
                    'supplier_item_code', 'item_description', 'quantity')   
        

class SsccAuditsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAudits
        fields = ('type', 'url', 'mandatory_audit_flag', 'sscc_labelled_correctly_flag',
                    'sscc_presented_correctly_flag','sscc','audit_comments', 'audited_by','audit_started_date_time','audit_completed_date_time' )
                    

class SsccDeliverySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccDelivery
        fields = ('type', 'url', 'first_scanned_date_time', 'sscc_audit_mandated_flag', 'first_scanned_by', 'sscc', )

        
class SsccGoodsReceiptSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccGoodsReceipt
        fields = ('type', 'url', 'goods_receipt_reference', 'goods_receipting_process_name', 'sscc', 
                    'goods_receipted_date_time', 'goods_receipted_by', 'goods_receipt_reference_date' )


class SsccAuditsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccAudits
        fields = ('type', 'url', 'mandatory_audit_flag', 'sscc_labelled_correctly_flag',
                    'sscc_presented_correctly_flag','sscc','audit_comments', 'audited_by','audit_started_date_time','audit_completed_date_time' )

                    
class SsccMandatoryAuditControlSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccMandatoryAuditControl
        fields = ('type', 'url', 'mitre_10_supplier_code', 'mitre_10_store_code',
                    'audit_every_nth_sscc','count_since_last_audit','supplier_certification_status', 
                    'recount_dollar_threshold','recount_dollar_percent_threshold',
                    'expected_deliveries_in_quiet_month', 'previous_guaranteed_monthly_audit_date_time', )
                    
                    
class SsccProductItemsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SsccProductItems
        fields = ('type', 'url', 'item_barcode', 'sscc', 'mitre_10_item_code',
                    'supplier_item_code','item_description','quantity', )


class SynchronisationsSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Synchronisations
        fields = ('type', 'url', 'client_identifier', 'start_event_date_time', 'start_control_id',
                    'synchronisation_type',)

                    
class SynchronisationsEndSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SynchronisationsEnd
        fields = ('type', 'url', 'sync', 'finish_event_date_time', 'finishing_control_id',
                    'synchronisation_type',)


class UnrecognisedSsccSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = UnrecognisedSscc
        fields = ('type', 'url', 'sscc_barcode', 'scanned_date_time', 'scanned_by',)
                    