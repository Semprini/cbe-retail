from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.job_management.models import Job, JobPartyRole


class JobSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Job
        fields = ('type', 'url', 'created', 'valid_from', 'valid_to', 
                    'job_number', 'account','job_status','credit','job_party_roles', )


class JobPartyRoleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = JobPartyRole
        fields = ('type', 'url', 'name', 'party', 'job', 'credit', )