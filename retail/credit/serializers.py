from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.credit.models import CreditBalanceEvent, CreditProfile


class CreditBalanceEventSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CreditBalanceEvent
        fields = ('type', 'url', 'customer', 'account', 'store', 'sale', 'datetime',
                  'amount', 'balance', )


class CreditProfileSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CreditProfile
        fields = ('type', 'url', 'customer', 'credit_agency', 'valid_from', 'valid_to','created',
                  'credit_risk_rating','credit_score',)


