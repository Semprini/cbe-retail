import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.job_management.models import Job, JobPartyRole
from retail.job_management.serializers import JobSerializer, JobPartyRoleSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobPartyRoleViewSet(viewsets.ModelViewSet):
    queryset = JobPartyRole.objects.all()
    serializer_class = JobPartyRoleSerializer    