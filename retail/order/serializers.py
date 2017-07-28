from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.order.models import Order, OrderItem, Quote, Estimate


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Order
        fields = ('type', 'url', 'channel', 'location', 'seller', 'datetime', 'order_type',
                  'total_amount', 'total_amount_excl', 'total_discount', 'total_tax',
                  'customer', 'account', 'promotion', 
                  'price_channel', 'price_calculation', 'order_items',)


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = OrderItem
        fields = ('type', 'url', 'order', 'product_offering', 'amount',
                  'discount','promotion' )


