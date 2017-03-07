from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.sale.models import RetailChannel, Sale, SaleItem, TenderType, Tender


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Sale
        fields = ('type', 'url', 'channel', 'store', 'datetime', 'docket_number',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'identification', 'promotion','till', 'staff', 
                  'price_channel', 'price_calculation', 'tenders','sale_items',)


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SaleItem
        fields = ('type', 'url', 'sale', 'product', 'amount',
                  'discount','promotion' )


class TenderTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = TenderType
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', )


class TenderSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Tender
        fields = ('type', 'url', 'sale', 'tender_type', 'amount',
                  'reference', )
                  
                  
class RetailChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = RetailChannel
        fields = ('type', 'url', 'name',)
                  
                  
          