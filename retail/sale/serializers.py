from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from drf_nest.serializers import ExtendedHyperlinkedSerialiser, LimitDepthMixin
from drf_nest.serializer_fields import TypeField, GenericRelatedField, ExtendedModelSerialiserField

from cbe.party.serializers import PartyRoleAssociationFromBasicSerializer, PartyRoleAssociationToBasicSerializer, IndividualSerializer, OrganisationSerializer
from cbe.party.models import Individual, Organisation, PartyRoleAssociation
from cbe.credit.serializers import CreditBalanceEventSerializer


from retail.store.models import Store
from retail.sale.models import SalesChannel, Sale, SaleItem, TenderType, Tender, Purchaser
from retail.product.serializers import ProductOfferingSerializer, ProductSerializer
from retail.pricing.serializers import ProductOfferingPriceSerializer


class TenderTypeSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    #type = TypeField()

    class Meta:
        model = TenderType
        fields = ('type', 'url', 'name', 'description', )


class TenderSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    #type = TypeField()
    #TODO: Waiting on pull request from django-rest
    #url = serializers.HyperlinkedIdentityField(view_name='tender-detail', read_only=False, queryset=Tender.objects.all())
    sale = serializers.HyperlinkedIdentityField(view_name='sale-detail', read_only=False)
    #sale = serializers.HyperlinkedIdentityField(view_name='sale-detail', queryset=Sale.objects.all(), required=False, allow_null=True, read_only=False)

    tender_type = ExtendedModelSerialiserField(TenderTypeSerializer())
    
    class Meta:
        model = Tender
        fields = ('type', 'url', 'sale', 'tender_type', 'amount', 'reference', )

    def to_internal_value(self, data):
        print( "VALIDATE2:{}".format(data) )
        return super(self.__class__, self).to_internal_value(data)

    def create(self, validated_data):
        print( "CREATE2:{}".format(validated_data) )
        return Tender.objects.create(**validated_data)
        

class SaleItemSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    #type = TypeField()
    #TODO: Waiting on pull request from django-rest
    #url = serializers.HyperlinkedIdentityField(view_name='saleitem-detail', read_only=False, queryset=SaleItem.objects.all())
    product = ExtendedModelSerialiserField(ProductSerializer())
    product_offering_price = ProductOfferingPriceSerializer()
    
    class Meta:
        model = SaleItem
        fields = ('type', 'url', 'sale', 'product_offering', 'product', 'price_channel', 'price_calculation',
                    'product_offering_price', 'quantity', 'unit_of_measure', 'amount',
                    'discount','promotion','cost_price' )

                  
class SaleSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    #type = TypeField()
    sale_items = SaleItemSerializer( many=True )
    tenders = TenderSerializer( many=True, read_only=False )
    credit_balance_events = CreditBalanceEventSerializer( many=True )
    store = serializers.HyperlinkedRelatedField(view_name='store-detail', lookup_field='enterprise_id', queryset=Store.objects.all())
    vendor = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
    
    class Meta:
        model = Sale
        fields = ('type', 'url', 'channel', 'store', 'vendor', 'datetime', 'docket_number',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'job', 'purchaser', 'identification', 'promotion','till', 'staff', 
                  'tenders', 'credit_balance_events', 'sale_items',)
       
    def to_internal_value(self, data):
        print( "VALIDATE:{}".format(data) )
        return super(self.__class__, self).to_internal_value(data)
        
    def create(self, validated_data):
        print( "CREATE2:{}".format(validated_data) )
        tenders_data = validated_data.pop('tenders')
        credit_balance_events_data = validated_data.pop('credit_balance_events')
        sale_items_data = validated_data.pop('sale_items')
        sale = Sale(**validated_data)
        
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

        # TODO: sale.pre_signal_xtra_related['credit_event'] = (credit_event,'sale')
        sale.save()
        return sale             

    def update(self, instance, validated_data):
        tenders_data = validated_data.pop('tenders')
        credit_balance_events_data = validated_data.pop('credit_balance_events')
        sale_items_data = validated_data.pop('sale_items')
        
        for key, value in validated_data.items():
            setattr( instance, key, value )
        
        tenders = instance.tenders.all()
        
        for tender_data in tenders_data:
            print( "Checking %s" %tender_data )
            # Are we updating or creating the nested object?
            if 'url' in tender_data.keys():
                resolved_func, unused_args, resolved_kwargs = resolve(urlparse(tender_data['url']).path)
                object = resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])
                print( "Updating %s" %object )
                for key, value in tender_data.items():
                    setattr( object, key, value )
                object.save()
            else:
                #TODO: Waiting on pull request from django-rest
                #object = Tender.objects.create(sale=instance, **tender_data)
                print( "Created (not)" )
            
            #TODO: Remove found tenders from the list of tenders and if partial remove any outstanding ones
        if self.partial == True:
            print("PARTIAL")

        instance.save()
        
        return instance             
        

class SalesChannelSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    #type = TypeField()

    class Meta:
        model = SalesChannel
        fields = ('type', 'url', 'name',)
                  
                  
class PurchaserSerializer(LimitDepthMixin, ExtendedHyperlinkedSerialiser):
    party = GenericRelatedField( many=False, 
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })
    type = TypeField()

    associations_from = GenericRelatedField( many=True, serializer_dict={PartyRoleAssociation: PartyRoleAssociationFromBasicSerializer(), } )
    associations_to = GenericRelatedField( many=True, serializer_dict={ PartyRoleAssociation: PartyRoleAssociationToBasicSerializer(), } )
    
    class Meta:
        model = Purchaser
        fields = ('type', 'url', 'party', 'credit', 'associations_from', 'associations_to',)

