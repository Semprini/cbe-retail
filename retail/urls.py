"""retail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from cbe.urls import cberouter

import retail.product.views as ProductViews
import retail.sale.views as SaleViews
import retail.loyalty.views as LoyaltyViews

admin.site.site_title = 'CBE Retail'
admin.site.site_header = 'Retail Business Entities'

retailrouter = DefaultRouter()
retailrouter.register(r'product/product_offering', ProductViews.ProductOfferingViewSet)
retailrouter.register(r'product/product_category', ProductViews.ProductCategoryViewSet)
retailrouter.register(r'product/promotion', ProductViews.PromotionViewSet)

retailrouter.register(r'sale/sale', SaleViews.SaleViewSet)
retailrouter.register(r'sale/sale_item', SaleViews.SaleItemViewSet)
retailrouter.register(r'sale/tender', SaleViews.TenderViewSet)
retailrouter.register(r'sale/tender_type', SaleViews.TenderTypeViewSet)

retailrouter.register(r'loyalty/loyalty_transaction', LoyaltyViews.LoyaltyTransactionViewSet)
retailrouter.register(r'loyalty/loyalty_scheme', LoyaltyViews.LoyaltySchemeViewSet)
retailrouter.register(r'loyalty/loyalty_card_type', LoyaltyViews.LoyaltyCardTypeViewSet)
retailrouter.register(r'loyalty/loyalty_card', LoyaltyViews.LoyaltyCardViewSet)

router = DefaultRouter()
for route in retailrouter.registry:
    router.register(route[0], route[1])
for route in cberouter.registry:
    router.register(route[0], route[1])
    
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    ]
