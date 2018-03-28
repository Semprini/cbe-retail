from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from drf_nest.serializer_fields import TypeField
from cbe.human_resources.serializers import IdentificationSerializer
from cbe.physical_object.serializers import StructureSerializer
from cbe.location.serializers import LocationSerializer, GeographicAreaSerializer
from cbe.party.serializers import OrganisationSerializer

from cbe.location.models import GeographicArea, Location
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

    def create(self, validated_data):
        tenders_data = validated_data.pop('identifiers', None)
        tenders_data = validated_data.pop('buildings', None)
        trade_area_data = validated_data.pop('trade_area', None)
        retail_area_data = validated_data.pop('retail_area', None)
        national_area_data = validated_data.pop('national_area', None)
        location_data = validated_data.pop('location', None)
        
        store = Store(**validated_data)
        
        if location_data:
            store.location, created = Location.objects.get_or_create(**location_data)
        if trade_area_data:
            store.trade_area, created = GeographicArea.objects.get_or_create(**trade_area_data)
        if retail_area_data:
            store.retail_area, created = GeographicArea.objects.get_or_create(**retail_area_data)
        if national_area_data:
            store.national_area, created = GeographicArea.objects.get_or_create(**national_area_data)
            
        store.save()
        return store
        
    def update(self, instance, validated_data):
        tenders_data = validated_data.pop('identifiers', None)
        tenders_data = validated_data.pop('buildings', None)
        trade_area_data = validated_data.pop('trade_area', None)
        retail_area_data = validated_data.pop('retail_area', None)
        national_area_data = validated_data.pop('national_area', None)
        location_data = validated_data.pop('location', None)

        for key, value in validated_data.items():
            setattr( instance, key, value )

        if location_data:
            instance.location, created = Location.objects.get_or_create(**location_data)
        if trade_area_data:
            instance.trade_area, created = GeographicArea.objects.get_or_create(**trade_area_data)
        if retail_area_data:
            instance.retail_area, created = GeographicArea.objects.get_or_create(**retail_area_data)
        if national_area_data:
            instance.national_area, created = GeographicArea.objects.get_or_create(**national_area_data)
            
        instance.save()
        return instance   