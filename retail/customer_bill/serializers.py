from urllib.parse import urlparse

from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from drf_nest.serializer_fields import TypeField
from cbe.customer.serializers import CustomerAccountSerializer
from cbe.party.models import Organisation

from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, ServiceCharge
from retail.customer_bill.models import AccountBillItem, JobBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
from retail.job_management.serializers import JobSerializer                 
                  
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


class AccountBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = AccountBillItem
        fields = '__all__'
        
class JobBillItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    job = JobSerializer()

    class Meta:
        model = JobBillItem
        fields = '__all__'


class CustomerBillSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    account = CustomerAccountSerializer(read_only=True)
    accountbillitems = AccountBillItemSerializer(many=True)
    jobbillitems = JobBillItemSerializer(many=True)
    
    class Meta:
        model = CustomerBill
        fields = ('type','url','account','specification','customer','number','created','period_from','period_to','status',
                    'amount','discounted','adjusted','rebated','disputed','allocated','accountbillitems','jobbillitems','servicebillitems')

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        accountbillitems_data = validated_data.pop('accountbillitems')
        jobbillitems_data = validated_data.pop('jobbillitems')
        bill = CustomerBill.objects.create(**validated_data)
        
         #TODO sub objects
        return bill             

    def update(self, instance, validated_data):
        #account_data = validated_data.pop('account')
        accountbillitems_data = validated_data.pop('accountbillitems')
        jobbillitems_data = validated_data.pop('jobbillitems')
        
        for key, value in validated_data.items():
            setattr( instance, key, value )
        
        if self.partial == True:
            print("PARTIAL")

        instance.save()
        return instance                     
                    
        
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
    home_store = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
    satellite_store = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = ServiceCharge
        fields = '__all__'