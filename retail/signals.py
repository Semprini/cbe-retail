from django.dispatch import receiver
from django.http import HttpRequest

from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer

import pika

from retail.settings import MQ_FRAMEWORK


def notify_extra_args(serializer, exchange_prefix, exchange_header_list, *args, **kwargs):
    def inner1(f, *args, **kwargs):
        def inner2(sender, instance, **kwargs):
            f(sender, instance, serializer=serializer, exchange_prefix=exchange_prefix, exchange_header_list=exchange_header_list, **kwargs)
        return inner2
    return inner1
    

def serializer_context():
    request = HttpRequest()
    request.META['SERVER_NAME'] = MQ_FRAMEWORK['HTTP_REST_CONTEXT']['SERVER_NAME']
    request.META['SERVER_PORT'] = MQ_FRAMEWORK['HTTP_REST_CONTEXT']['SERVER_PORT']
    return { 'request': Request(request), }
    
    
def notify_save_instance(sender, instance, created, serializer, exchange_prefix, exchange_header_list, **kwargs):
    """
    Generic notification of object change
    """
    if created:
        exchange_name = exchange_prefix + ".created"
    else:
        exchange_name = exchange_prefix + ".updated"

    headers_dict = {}
    for header in exchange_header_list:
        headers_dict[header] = getattr(instance,header)
            
    json = JSONRenderer().render(serializer(instance, context=serializer_context()).data).decode(encoding='utf-8')

    if MQ_FRAMEWORK['HOST'] == 'None':
        print("EXCHANGE=%s | HEADERS=%s="%(exchange_name, headers_dict))
        print('%s'%json)
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_FRAMEWORK['HOST']))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, type='headers')

        channel.basic_publish(  exchange=exchange_name,
                                routing_key='cbe',
                                body=json,
                                properties = pika.BasicProperties({'headers': headers_dict}))
        connection.close()    
