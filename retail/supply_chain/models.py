from __future__ import unicode_literals

from django.db import models

from cbe.supplier_partner.models import Supplier, Buyer
from retail.store.models import Store
from retail.product.models import Product

class Asns(models.Model):
    asn_reference = models.CharField(max_length=32, blank=True, null=True)
    message_date_time = models.DateTimeField(blank=True, null=True)
    message_received_date_time = models.DateTimeField(blank=True, null=True)
    despatch_date_time = models.DateTimeField(blank=True, null=True)
    shipment_due_date_time = models.DateTimeField(blank=True, null=True)
    final_shipment_flag = models.IntegerField(blank=True, null=True)

    purchase_order = models.ForeignKey( 'PurchaseOrder' )
    supplier = models.ForeignKey( Supplier, blank=True, null=True)
    buyer = models.ForeignKey( Buyer, blank=True, null=True)
    delivery_store = models.ForeignKey( Store, blank=True, null=True)

    class Meta:
        unique_together = (('asn_reference', 'supplier'),)


class PoExpectedDeliveryDate(models.Model):
    purchase_order = models.ForeignKey( 'PurchaseOrder', blank=True, null=True )
    expected_delivery_date = models.DateTimeField(blank=True, null=True)
    supplier = models.ForeignKey( Supplier, blank=True, null=True)
    message_received_date_time = models.DateTimeField(blank=True, null=True)
    source_record_table = models.CharField(max_length=31, blank=True, null=True)
    source_record_id = models.CharField(max_length=50, blank=True, null=True)
    delivery_store = models.ForeignKey( Store, blank=True, null=True)

    class Meta:
        unique_together = (('purchase_order', 'delivery_store', 'supplier'),)


class PurchaseOrderAcknowledgementLineItems(models.Model):
    purchase_order_acknowledgement = models.ForeignKey('PurchaseOrderAcknowledgements', models.DO_NOTHING)
    product = models.ForeignKey(Product, blank=True, null=True)
    supplier_item_code = models.CharField(db_column='supplier_item_Code', max_length=15, blank=True, null=True)  # Field name made lowercase.

    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=6, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    notification_code = models.IntegerField(blank=True, null=True)
    notification_description = models.CharField(max_length=50, blank=True, null=True)


class PurchaseOrderAcknowledgements(models.Model):
    poa_reference = models.CharField(max_length=32, blank=True, null=True)
    message_date_time = models.DateTimeField(blank=True, null=True)
    message_received_date_time = models.DateTimeField(blank=True, null=True)
    delivery_date_time_requested = models.DateTimeField(blank=True, null=True)
    delivery_date_time_estimated = models.DateTimeField(blank=True, null=True)

    purchase_order = models.ForeignKey( 'PurchaseOrder', blank=True, null=True )
    supplier = models.ForeignKey( Supplier, blank=True, null=True)
    buyer = models.ForeignKey( Buyer, blank=True, null=True)
    delivery_store = models.ForeignKey( Store, blank=True, null=True)

    message_function_code = models.IntegerField(blank=True, null=True)
    message_function_description = models.CharField(max_length=50, blank=True, null=True)
    latest_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('message_date_time', 'purchase_order', 'supplier', 'delivery_store'),)


class PurchaseOrderLineItems(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', models.DO_NOTHING)
    product = models.ForeignKey(Product, blank=True, null=True)
    supplier_item_code = models.CharField(max_length=15, blank=True, null=True)
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=6, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    conversion_factor = models.IntegerField(blank=True, null=True)


class PurchaseOrder(models.Model):
    purchase_order_reference = models.CharField(max_length=10, blank=True, null=True)
    supplier = models.ForeignKey( Supplier, blank=True, null=True)
    buyer = models.ForeignKey( Buyer, blank=True, null=True)
    delivery_store = models.ForeignKey( Store, blank=True, null=True)
    
    purchase_order_date = models.DateTimeField(blank=True, null=True)
    despatched_date_time = models.DateTimeField(blank=True, null=True)
    delivery_due_date = models.DateTimeField(blank=True, null=True)
    latest_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('purchase_order_reference', 'supplier', 'delivery_store', 'despatched_date_time'),)


class SchemaVersion(models.Model):
    installed_rank = models.IntegerField(primary_key=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    script = models.CharField(max_length=1000)
    checksum = models.IntegerField(blank=True, null=True)
    installed_by = models.CharField(max_length=100)
    installed_on = models.DateTimeField()
    execution_time = models.IntegerField()
    success = models.IntegerField()


class Sscc(models.Model):
    asn = models.ForeignKey(Asns, models.DO_NOTHING)
    sscc_barcode = models.CharField(unique=True, max_length=20, blank=True, null=True)
    package_type = models.CharField(max_length=20, blank=True, null=True)
    parent_sscc_barcode = models.CharField(max_length=20, blank=True, null=True)
    height_mm = models.FloatField(blank=True, null=True)
    width_mm = models.FloatField(blank=True, null=True)
    weight_kilos = models.FloatField(blank=True, null=True)
    length_mm = models.FloatField(blank=True, null=True)


class SsccAuditCorrectionActions(models.Model):
    audit_correction_action_type = models.CharField(max_length=50, blank=True, null=True)
    audit_correction_reference = models.CharField(max_length=50, blank=True, null=True)
    goods_receipt_reference_date = models.CharField(max_length=15, blank=True, null=True)
    sscc_audit_correction = models.ForeignKey('SsccAuditCorrections', models.DO_NOTHING, blank=True, null=True)


class SsccAuditCorrectionProductItems(models.Model):
    mitre_10_item_code = models.CharField(max_length=15, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sscc_audit_correction_action = models.ForeignKey(SsccAuditCorrectionActions, models.DO_NOTHING, blank=True, null=True)


class SsccAuditCorrectionReversal(models.Model):
    submitted_by = models.CharField(max_length=50, blank=True, null=True)
    submitted_date_time = models.DateTimeField(blank=True, null=True)
    sscc_audit_correction = models.ForeignKey('SsccAuditCorrections', models.DO_NOTHING, blank=True, null=True)


class SsccAuditCorrections(models.Model):
    sscc_audits = models.ForeignKey('SsccAudits', models.DO_NOTHING)


class SsccAuditProductItems(models.Model):
    sscc_audit = models.ForeignKey('SsccAudits', models.DO_NOTHING)
    item_barcode = models.CharField(max_length=20, blank=True, null=True)
    mitre10_item_code = models.CharField(max_length=15, blank=True, null=True)
    supplier_item_code = models.CharField(max_length=15, blank=True, null=True)
    item_description = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class SsccAudits(models.Model):
    mandatory_audit_flag = models.IntegerField()
    sscc_labelled_correctly_flag = models.IntegerField()
    sscc_presented_correctly_flag = models.IntegerField()
    sscc = models.ForeignKey(Sscc, models.DO_NOTHING)
    audit_comments = models.CharField(max_length=2000, blank=True, null=True)
    audited_by = models.CharField(max_length=50, blank=True, null=True)
    audit_started_date_time = models.DateTimeField(blank=True, null=True)
    audit_completed_date_time = models.DateTimeField(blank=True, null=True)


class SsccDelivery(models.Model):
    first_scanned_date_time = models.DateTimeField(blank=True, null=True)
    sscc_audit_mandated_flag = models.IntegerField(blank=True, null=True)
    first_scanned_by = models.CharField(max_length=50, blank=True, null=True)
    sscc = models.ForeignKey(Sscc, models.DO_NOTHING)


class SsccGoodsReceipt(models.Model):
    goods_receipt_reference = models.CharField(max_length=50, blank=True, null=True)
    goods_receipting_process_name = models.CharField(max_length=5, blank=True, null=True)
    sscc = models.ForeignKey(Sscc, models.DO_NOTHING, blank=True, null=True)
    goods_receipted_date_time = models.DateTimeField(blank=True, null=True)
    goods_receipted_by = models.CharField(max_length=50, blank=True, null=True)
    goods_receipt_reference_date = models.CharField(max_length=15, blank=True, null=True)


class SsccMandatoryAuditControl(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    mitre_10_supplier_code = models.CharField(max_length=15, blank=True, null=True)
    mitre_10_store_code = models.CharField(max_length=10, blank=True, null=True)
    audit_every_nth_sscc = models.IntegerField(blank=True, null=True)
    count_since_last_audit = models.IntegerField(blank=True, null=True)
    supplier_certification_status = models.CharField(max_length=50, blank=True, null=True)
    recount_dollar_threshold = models.FloatField(blank=True, null=True)
    recount_dollar_percent_threshold = models.FloatField(blank=True, null=True)
    expected_deliveries_in_quiet_month = models.IntegerField(blank=True, null=True)
    previous_guaranteed_monthly_audit_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('mitre_10_supplier_code', 'mitre_10_store_code'),)


class SsccProductItems(models.Model):
    item_barcode = models.CharField(max_length=15, blank=True, null=True)
    sscc = models.ForeignKey(Sscc, models.DO_NOTHING, blank=True, null=True)
    mitre_10_item_code = models.CharField(max_length=15, blank=True, null=True)
    supplier_item_code = models.CharField(max_length=15, blank=True, null=True)
    item_description = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class Synchronisations(models.Model):
    client_identifier = models.CharField(max_length=100, blank=True, null=True)
    start_event_date_time = models.DateTimeField(unique=True, blank=True, null=True)
    start_control_id = models.IntegerField(blank=True, null=True)
    synchronisation_type = models.CharField(max_length=50, blank=True, null=True)


class SynchronisationsEnd(models.Model):
    sync = models.OneToOneField(Synchronisations, models.DO_NOTHING, primary_key=True)
    finish_event_date_time = models.DateTimeField(unique=True, blank=True, null=True)
    finishing_control_id = models.IntegerField(blank=True, null=True)
    synchronisation_type = models.CharField(max_length=50, blank=True, null=True)


class UnrecognisedSscc(models.Model):
    sscc_barcode = models.CharField(max_length=20, blank=True, null=True)
    scanned_date_time = models.DateTimeField(blank=True, null=True)
    scanned_by = models.CharField(max_length=50, blank=True, null=True)

