[![Build Status](https://img.shields.io/circleci/project/github/Semprini/cbe-retail.svg)](https://circleci.com/gh/Semprini/cbe-retail)  [![Docker](http://dockeri.co/image/semprini/cbe-retail)](https://hub.docker.com/r/semprini/cbe-retail/)

# cbe-retail
Extensions to the Common Business Entities framework for Retail Operations. See [Semprini/cbe](https://github.com/Semprini/cbe) for more details.

CBE provides RESTful CRUD and administration for common business entities persisted on relational DBs and (coming soon) NoSQL DBs. This polyglot persistence model forms the backbone of an organisations master data governance. The rationale is discussed in the [Wiki](https://github.com/Semprini/cbe/wiki).

# Why?
The most common & costly architectural issues seen in enterprises is legacy replacement big bang and integration tight coupling. To address this CBE-Retail provides master data governance which can be deployed as a data fabric, extending an API layer across back offices and stores without needing an integration bus as the schema is consistent. Perfect for a hybrid or cloud deployment model.

Unlike ERP based master data governance platforms like SAP MDG, CBE is built to be more practical and used as an operational data source. Micro-services architecture is providing the next generation of legacy transformation via specific units of business functionality. When developing a micro-services architecture data input & output needs to be thought about. A micro-service may have it's own database to provide decoupling but this often leads to inconsistent and unmanageable data throughout the organisation. CBE alleviates this by allowing micro-services to have no database and either receive or query the data layer via APIs which fulfils the micro-services requirements of independently deployable, scalable, decoupled etc.

With a common schema deployed accross the enterprise and exposed via a governed API layer many domains are simplified like integration, BI & reporting. One key to this is not to give ownership of business data to products but treat business data as it's own product which can be goverened and exposed independently. This effectively means the business is only coupled to it's own semantics.

Extensions include:
  - Store
  - Credit
  - Sale
  - Order
  - Product
  - Pricing
  - Customer Bill
  - Loyalty
  - Market
 
Entities inherited from CBE:
  - business_interaction
  - customer
  - location
  - party
  - trouble
  - physical_object
  - supplier_partner
  - resource
  - human_resources

