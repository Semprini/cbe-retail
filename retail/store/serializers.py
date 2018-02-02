from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.human_resources.serializers import IdentificationSerializer
from cbe.physical_object.serializers import StructureSerializer
from cbe.location.serializers import LocationSerializer, GeographicAreaSerializer
from cbe.party.serializers import OrganisationSerializer

from cbe.party.models import Organisation
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
    #organisation = OrganisationSerializer()
    organisation = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
    trade_area = GeographicAreaSerializer(required=False, allow_null=True)
    retail_area = GeographicAreaSerializer(required=False, allow_null=True)
    national_area = GeographicAreaSerializer(required=False, allow_null=True)
    
    class Meta:
        model = Store
        fields = (  'type', 'url', 'name', 'enterprise_id', 'code', 'store_type', 'store_class', 
                    'opening_date', 'identifiers', 'location', 'organisation', 'buildings', 
                    'trade_area', 'retail_area', 'national_area' )
        view_name = 'store-detail'

