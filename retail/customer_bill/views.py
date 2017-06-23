import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets

from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, AccountBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem
from retail.customer_bill.serializers import CustomerBillingCycleSerializer, CustomerBillSpecificationSerializer, CustomerBillSerializer
from retail.customer_bill.serializers import AccountBillItemSerializer, SubscriptionBillItemSerializer, ServiceBillItemSerializer, RebateBillItemSerializer, AllocationBillItemSerializer, AdjustmentBillItemSerializer, DisputeBillItemSerializer


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

    
class AccountBillItemViewSet(viewsets.ModelViewSet):
    queryset = AccountBillItem.objects.all()
    serializer_class = AccountBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    
    
    
class SubscriptionBillItemViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBillItem.objects.all()
    serializer_class = SubscriptionBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
class ServiceBillItemViewSet(viewsets.ModelViewSet):
    queryset = ServiceBillItem.objects.all()
    serializer_class = ServiceBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )        
    

class RebateBillItemViewSet(viewsets.ModelViewSet):
    queryset = RebateBillItem.objects.all()
    serializer_class = RebateBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
class AllocationBillItemViewSet(viewsets.ModelViewSet):
    queryset = AllocationBillItem.objects.all()
    serializer_class = AllocationBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
class AdjustmentBillItemViewSet(viewsets.ModelViewSet):
    queryset = AdjustmentBillItem.objects.all()
    serializer_class = AdjustmentBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
class DisputeBillItemViewSet(viewsets.ModelViewSet):
    queryset = DisputeBillItem.objects.all()
    serializer_class = DisputeBillItemSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
    