from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.store.models import Store


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Store
        fields = ('type', 'url', 'name', 'code', 'location', 'owner' )


