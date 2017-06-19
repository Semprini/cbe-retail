from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.market.models import MarketSegment, MarketStrategy


class MarketSegmentSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = MarketSegment
        fields = ('type', 'url', 'name' )

        
class MarketStrategySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = MarketStrategy
        fields = ('type', 'url', 'name' )        

