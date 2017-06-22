from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, AccountBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
                 
                  
class CustomerBillingCycleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CustomerBillingCycle
        fields = '__all__'

        
class CustomerBillSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CustomerBillSpecification
        fields = '__all__'


class CustomerBillSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CustomerBill
        fields = '__all__'

        
