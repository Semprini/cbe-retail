import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from retail.store.models import Store
from retail.store.serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_fields = ('store_type', 'store_class', 'code', 'trade_area', 'retail_area', 'national_area')
    lookup_field = 'enterprise_id'


