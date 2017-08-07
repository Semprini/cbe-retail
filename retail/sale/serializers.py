from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import PartyRelatedField, PartyRoleAssociationFromBasicSerializer, PartyRoleAssociationToBasicSerializer
from cbe.party.models import PartyRoleAssociation
from retail.sale.models import SalesChannel, Sale, SaleItem, TenderType, Tender, Purchaser


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Sale
        fields = ('type', 'url', 'channel', 'store', 'seller', 'datetime', 'docket_number',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'purchaser', 'identification', 'promotion','till', 'staff', 
                  'price_channel', 'price_calculation', 'tenders','credit_balance_events','sale_items',)


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SaleItem
        fields = ('type', 'url', 'sale', 'product_offering', 'amount',
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
                  
                  
class SalesChannelSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SalesChannel
        fields = ('type', 'url', 'name',)
                  
                  
class PurchaserSerializer(serializers.HyperlinkedModelSerializer):
    #party = GenericRelatedField( many=False, serializer_dict={
    #        Individual: IndividualSerializer(),
    #        Organisation: OrganisationSerializer(),
    #    })
    party = PartyRelatedField()
    type = TypeField()

    associations_from = GenericRelatedField( many=True, serializer_dict={PartyRoleAssociation: PartyRoleAssociationFromBasicSerializer(), } )
    associations_to = GenericRelatedField( many=True, serializer_dict={ PartyRoleAssociation: PartyRoleAssociationToBasicSerializer(), } )
    
    class Meta:
        model = Purchaser
        fields = ('type', 'url', 'party', 'transation_limit', 'associations_from', 'associations_to',)

