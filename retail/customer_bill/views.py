import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets

from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, AccountBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
from retail.customer_bill.serializers import CustomerBillingCycleSerializer, CustomerBillSpecificationSerializer, CustomerBillSerializer
#, AccountBillItemSerializer, SubscriptionBillItemSerializer, ServiceBillItemSerializer, RebateBillItemSerializer, AllocationBillItemSerializer, AdjustmentBillItemSerializer, DisputeBillItemSerializer


class CustomerBillingCycleViewSet(viewsets.ModelViewSet):
    queryset = CustomerBillingCycle.objects.all()
    serializer_class = CustomerBillingCycleSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
    
class CustomerBillSpecificationViewSet(viewsets.ModelViewSet):
    queryset = CustomerBillSpecification.objects.all()
    serializer_class = CustomerBillSpecificationSerializer
    permission_classes = (permissions.DjangoModelPermissions, )


class CustomerBillViewSet(viewsets.ModelViewSet):
    queryset = CustomerBill.objects.all()
    serializer_class = CustomerBillSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    