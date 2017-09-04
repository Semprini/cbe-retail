from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings
    
class CustomerBillConfig(AppConfig):
    name = 'retail.customer_bill'

    def __init__(self, app_name, app_module):
        super(self.__class__, self).__init__(app_name, app_module)
    
    def ready(self):
        import cbe.signals
        from retail.customer_bill.models import CustomerBill
        from retail.customer_bill.serializers import CustomerBillSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('status',)
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=CustomerBillSerializer, 
                                                                exchange_prefix=exchange_prefix + ".CustomerBill",
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=CustomerBill, weak=False)
