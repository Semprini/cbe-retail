from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.human_resources.serializers import IdentificationSerializer
from cbe.physical_object.serializers import StructureSerializer
from cbe.location.serializers import LocationSerializer
from cbe.party.serializers import OrganisationSerializer

from retail.store.models import Store


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    url = serializers.HyperlinkedIdentityField(
        view_name='store-detail',
        lookup_field='enterprise_id'
    )
    identifiers = IdentificationSerializer(many=True,)
    buildings = StructureSerializer(many=True,)
    location = LocationSerializer(required=False, allow_null=True)
    organisation = OrganisationSerializer()
    
    class Meta:
        model = Store
        fields = ('type', 'url', 'name', 'enterprise_id', 'code', 'store_type', 'store_class', 'opening_date', 'identifiers', 'location', 'organisation', 'buildings' )
        view_name = 'store-detail'

