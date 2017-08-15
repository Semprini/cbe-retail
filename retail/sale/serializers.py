from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import PartyRelatedField, PartyRoleAssociationFromBasicSerializer, PartyRoleAssociationToBasicSerializer
from cbe.party.models import PartyRoleAssociation
from cbe.credit.serializers import CreditBalanceEventSerializer

from retail.sale.models import SalesChannel, Sale, SaleItem, TenderType, Tender, Purchaser
from retail.product.serializers import ProductOfferingSerializer


class TenderTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = TenderType
        fields = ('type', 'url', 'valid_from', 'valid_to', 'name',
                  'description', )


class TenderSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #TODO: Waiting on pull request from django-rest
    #url = serializers.HyperlinkedIdentityField(view_name='tender-detail', read_only=False, queryset=Tender.objects.all())

    class Meta:
        model = Tender
        fields = ('type', 'url', 'sale', 'tender_type', 'amount',
                  'reference', )

                  
class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #TODO: Waiting on pull request from django-rest
    #url = serializers.HyperlinkedIdentityField(view_name='saleitem-detail', read_only=False, queryset=SaleItem.objects.all())
    product_offering = ProductOfferingSerializer()
    
    class Meta:
        model = SaleItem
        fields = ('type', 'url', 'sale', 'product_offering', 'amount',
                  'discount','promotion' )

                  
class SaleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    sale_items = SaleItemSerializer( many=True )
    tenders = TenderSerializer( many=True, read_only=False )
    credit_balance_events = CreditBalanceEventSerializer( many=True )
    url = serializers.HyperlinkedIdentityField(view_name='sale-detail', read_only=True)
    
    class Meta:
        model = Sale
        fields = ('type', 'url', 'channel', 'store', 'seller', 'datetime', 'docket_number',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'purchaser', 'identification', 'promotion','till', 'staff', 
                  'price_channel', 'price_calculation', 'tenders', 'credit_balance_events', 'sale_items',)
        
    def create(self, validated_data):
        tenders_data = validated_data.pop('tenders')
        #credit_balance_events_data = validated_data.pop('credit_balance_events')
        sale_items_data = validated_data.pop('sale_items')
        sale = Sale.objects.create(**validated_data)
        
        for tender_data in tenders_data:
            # Are we updating or creating the nested object?
            if 'url' in tender_data.keys():
                resolved_func, unused_args, resolved_kwargs = resolve(
                    urlparse(tender_data['url']).path)
                object = resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])
                for key, value in tender_data.items():
                    setattr( object, key, value )  
            else:
                Tender.objects.create(sale=sale, **tender_data)
        return sale             

    def update(self, instance, validated_data):
        tenders_data = validated_data.pop('tenders')
        #credit_balance_events_data = validated_data.pop('credit_balance_events')
        sale_items_data = validated_data.pop('sale_items')
        
        for key, value in validated_data.items():
            setattr( instance, key, value )
        
        tenders = instance.tenders.all()
        
        for tender_data in tenders_data:
            print( "Checking %s" %tender_data )
            # Are we updating or creating the nested object?
            if 'url' in tender_data.keys():
                resolved_func, unused_args, resolved_kwargs = resolve(
                    urlparse(tender_data['url']).path)
                object = resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])
                print( "Updating %s" %object )
                for key, value in tender_data.items():
                    setattr( object, key, value )  
            else:
                #TODO: Waiting on pull request from django-rest
                #object = Tender.objects.create(sale=instance, **tender_data)
                print( "Created (not)" )
            
            #TODO: Remove found tenders from the list of tenders and if partial remove any outstanding ones
        if self.partial == True:
            print("PARTIAL")

        return instance             
        

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
        fields = ('type', 'url', 'party', 'credit', 'associations_from', 'associations_to',)

