from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from drf_nest.serializer_fields import TypeField
from cbe.party.models import Organisation

from retail.order.models import Order, OrderItem, Quote, Estimate
from retail.store.models import Store


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    store = serializers.HyperlinkedRelatedField(view_name='store-detail', lookup_field='enterprise_id', queryset=Store.objects.all())
    seller = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = Order
        fields = ('type', 'url', 'channel', 'store', 'seller', 'datetime', 'order_type',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'promotion', 
                  'price_channel', 'price_calculation', 'order_items',)

                  
class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    store = serializers.HyperlinkedRelatedField(view_name='store-detail', lookup_field='enterprise_id', queryset=Store.objects.all())
    seller = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = Quote
        fields = ('type', 'url', 'channel', 'store', 'seller', 'datetime', 'order_type',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'promotion', 
                  'price_channel', 'price_calculation', 'order_items',)


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = OrderItem
        fields = ('type', 'url', 'order', 'product_offering', 'amount',
                  'discount','promotion' )


