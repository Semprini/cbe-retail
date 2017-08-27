from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.customer.serializers import CustomerAccountSerializer
from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, ServiceCharge
from retail.customer_bill.models import AccountBillItem, JobBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
                 
                  
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
    account = CustomerAccountSerializer()
    
    class Meta:
        model = CustomerBill
        fields = ('type','url','account','specification','customer','number','created','period_from','period_to','status',
                    'amount','discounted','adjusted','rebated','disputed','allocated','accountbillitems','jobbillitems')

        
class AccountBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = AccountBillItem
        fields = '__all__'
        
class JobBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = JobBillItem
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
        
        
class ServiceChargeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = ServiceCharge
        fields = '__all__'