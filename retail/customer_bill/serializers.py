from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill
from retail.customer_bill.models import AccountBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
                 
                  
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

        
class Serializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CustomerBill
        fields = '__all__'
        

class AccountBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = AccountBillItem
        fields = '__all__'
        
class SubscriptionBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = SubscriptionBillItem
        fields = '__all__'
        
class ServiceBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ServiceBillItem
        fields = '__all__'
        
class RebateBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = RebateBillItem
        fields = '__all__'
        
class AllocationBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = AllocationBillItem
        fields = '__all__'
        
        
class AdjustmentBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = AdjustmentBillItem
        fields = '__all__'
        
        
class DisputeBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = DisputeBillItem
        fields = '__all__'
        
