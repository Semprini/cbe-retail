python manage.py graph_models -I Place,Country,City,Province,GeographicAddress,UrbanPropertyAddress,UrbanPropertySubAddress,RuralPropertyAddress,RuralPropertySubAddress,PoBoxAddress,Location  > ./docs/uml/location.dot
dot ./docs/uml/location.dot -Tpng -o./docs/uml/location.png

python manage.py graph_models -I ProductCategory,ProductAssociation,Product,ProductSpecification,SupplierProduct,ProductOffering,ProductStock,ProductStockTake,Location,Organisation,Staff,Supplier,Store > ./docs/uml/product.dot
dot ./docs/uml/product.dot -Tpng -o./docs/uml/product.png

python manage.py graph_models -I Purchaser,SalesChannel,Sale,SaleItem,TenderType,Tender,Organisation,Customer,CustomerAccount,PhysicalResource,Staff,Identification,Credit,CreditBalanceEvent,Store,Product,ProductOffering,Job > ./docs/uml/sale.dot
dot ./docs/uml/sale.dot -Tpng -o./docs/uml/sale.png

python manage.py graph_models -I Product,ProductOffering,ProductOfferingPrice,PriceChannel,PriceCalculation,Promotion > ./docs/uml/pricing.dot
dot ./docs/uml/pricing.dot -Tpng -o./docs/uml/pricing.png

python manage.py graph_models -I Asns,PoExpectedDeliveryDate,PurchaseOrderAcknowledgementLineItems,PurchaseOrderAcknowledgements,PurchaseOrderLineItems,PurchaseOrder,Sscc,SsccAuditCorrectionActions,SsccAuditCorrectionProductItems,SsccAuditCorrectionReversal,SsccAuditCorrections,SsccAuditProductItems,SsccAudits,SsccDelivery,SsccGoodsReceipt,SsccMandatoryAuditControl,SsccProductItems,UnrecognisedSscc > ./docs/uml/supply_chain.dot
dot ./docs/uml/supply_chain.dot -Tpng -o./docs/uml/supply_chain.png

python manage.py graph_models -I CustomerBillingCycle,CustomerBillSpecification,CustomerBill,CustomerBillItem,AccountBillItem,JobBillItem,SubscriptionBillItem,ServiceBillItem,RebateBillItem,AllocationBillItem,AdjustmentBillItem,DisputeBillItem,ServiceCharge,Customer,CustomerAccount,Sale,Job,CustomerPayment > ./docs/uml/customer_bill.dot
dot ./docs/uml/customer_bill.dot -Tpng -o./docs/uml/customer_bill.png

python manage.py graph_models -I PartyRole,Party,Individual,Organisation,Customer,CustomerAccount,CustomerAccountContact,CustomerAccountRelationship > ./docs/uml/customer.dot
dot ./docs/uml/customer.dot -Tpng -o./docs/uml/customer.png

python manage.py graph_models -I TroubleTicket,TroubleTicketItem,Problem,ResourceAlarm,TrackingRecord,BusinessInteraction,BusinessInteractionItem > ./docs/uml/trouble.dot
dot ./docs/uml/trouble.dot -Tpng -o./docs/uml/trouble.png

python manage.py graph_models -I Order,OrderItem,Product,Quote,Estimate,Organisation,Customer,CustomerAccount,Store,SalesChannel,Location,ProductOffering,PriceChannel,PriceCalculation,Promotion > ./docs/uml/order.dot
dot ./docs/uml/order.dot -Tpng -o./docs/uml/order.png

python manage.py graph_models -I Resource,PhysicalResource,LogicalResource,ResourceOrder,ResourceOrderItem,BusinessInteraction,BusinessInteractionItem,PhysicalObject,ManufacturedObject,Structure,Vehicle,Device > ./docs/uml/resource.dot
dot ./docs/uml/resource.dot -Tpng -o./docs/uml/resource.png
