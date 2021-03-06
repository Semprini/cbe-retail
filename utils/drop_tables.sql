SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'data';

USE data
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS auth_group;                                        
DROP TABLE IF EXISTS auth_group_permissions;                            
DROP TABLE IF EXISTS auth_permission;                                   
DROP TABLE IF EXISTS auth_user;                                         
DROP TABLE IF EXISTS auth_user_groups;                                  
DROP TABLE IF EXISTS auth_user_user_permissions;                        
DROP TABLE IF EXISTS django_admin_log;                                  
DROP TABLE IF EXISTS django_content_type;                               
DROP TABLE IF EXISTS django_migrations;                                 
DROP TABLE IF EXISTS django_session;                                    
DROP TABLE IF EXISTS django_site;                                       
DROP TABLE IF EXISTS explorer_query;
DROP TABLE IF EXISTS explorer_querylog;
DROP TABLE IF EXISTS socialaccount_socialaccount;                       
DROP TABLE IF EXISTS socialaccount_socialapp;                           
DROP TABLE IF EXISTS socialaccount_socialapp_sites;                     
DROP TABLE IF EXISTS socialaccount_socialtoken;                         
DROP TABLE IF EXISTS account_emailaddress;                              
DROP TABLE IF EXISTS account_emailconfirmation;                         

DROP TABLE IF EXISTS forecast_merchdate;                                
DROP TABLE IF EXISTS forecast_merchweek;                                
DROP TABLE IF EXISTS forecast_productforecast;                          
DROP TABLE IF EXISTS forecast_productsaleweek;                          
DROP TABLE IF EXISTS forecast_storeproductsaleweek;                          

DROP TABLE IF EXISTS accounts_receivable_customerpayment;               
DROP TABLE IF EXISTS accounts_receivable_paymentchannel;                
DROP TABLE IF EXISTS credit_credit;                                     
DROP TABLE IF EXISTS credit_creditalert;                                
DROP TABLE IF EXISTS credit_creditbalanceevent;                         
DROP TABLE IF EXISTS credit_creditprofile;                              
DROP TABLE IF EXISTS customer_bill_accountbillitem;                     
DROP TABLE IF EXISTS customer_bill_accountbillitem_sale_events;         
DROP TABLE IF EXISTS customer_bill_adjustmentbillitem;                  
DROP TABLE IF EXISTS customer_bill_adjustmentbillitem_sale_events;      
DROP TABLE IF EXISTS customer_bill_allocationbillitem;                  
DROP TABLE IF EXISTS customer_bill_allocationbillitem_sale_events;      
DROP TABLE IF EXISTS customer_bill_customerbill;                        
DROP TABLE IF EXISTS customer_bill_customerbillingcycle;                
DROP TABLE IF EXISTS customer_bill_customerbillspecification;           
DROP TABLE IF EXISTS customer_bill_disputebillitem;                     
DROP TABLE IF EXISTS customer_bill_disputebillitem_sale_events;         
DROP TABLE IF EXISTS customer_bill_jobbillitem;                         
DROP TABLE IF EXISTS customer_bill_jobbillitem_sale_events;             
DROP TABLE IF EXISTS customer_bill_rebatebillitem;                      
DROP TABLE IF EXISTS customer_bill_rebatebillitem_sale_events;          
DROP TABLE IF EXISTS customer_bill_servicebillitem;                     
DROP TABLE IF EXISTS customer_bill_servicebillitem_sale_events;         
DROP TABLE IF EXISTS customer_bill_servicecharge;                       
DROP TABLE IF EXISTS customer_bill_servicecharge_sales;                 
DROP TABLE IF EXISTS customer_bill_subscriptionbillitem;                
DROP TABLE IF EXISTS customer_bill_subscriptionbillitem_sale_events;    
DROP TABLE IF EXISTS customer_customer;                                 
DROP TABLE IF EXISTS customer_customer_email_contacts;                  
DROP TABLE IF EXISTS customer_customer_logical_resources;               
DROP TABLE IF EXISTS customer_customer_physical_contacts;               
DROP TABLE IF EXISTS customer_customer_physical_resources;              
DROP TABLE IF EXISTS customer_customer_telephone_numbers;               
DROP TABLE IF EXISTS customer_customeraccount;                          
DROP TABLE IF EXISTS customer_customeraccount_customer_account_contact; 
DROP TABLE IF EXISTS customer_customeraccountcontact;                   
DROP TABLE IF EXISTS customer_customeraccountcontact_email_contacts;    
DROP TABLE IF EXISTS customer_customeraccountcontact_logical_resources; 
DROP TABLE IF EXISTS customer_customeraccountcontact_physical_contacts; 
DROP TABLE IF EXISTS customer_customeraccountcontact_physical_resources;
DROP TABLE IF EXISTS customer_customeraccountcontact_telephone_numbers; 
DROP TABLE IF EXISTS customer_customeraccountrelationship;              
DROP TABLE IF EXISTS human_resources_identification;                    
DROP TABLE IF EXISTS human_resources_identificationtype;                
DROP TABLE IF EXISTS human_resources_staff;                             
DROP TABLE IF EXISTS human_resources_staff_email_contacts;              
DROP TABLE IF EXISTS human_resources_staff_logical_resources;           
DROP TABLE IF EXISTS human_resources_staff_physical_contacts;           
DROP TABLE IF EXISTS human_resources_staff_physical_resources;          
DROP TABLE IF EXISTS human_resources_staff_telephone_numbers;           
DROP TABLE IF EXISTS human_resources_timesheet;                         
DROP TABLE IF EXISTS human_resources_timesheetentry;                    
DROP TABLE IF EXISTS information_technology_component;                  
DROP TABLE IF EXISTS information_technology_component_classification;   
DROP TABLE IF EXISTS information_technology_component_processes;        
DROP TABLE IF EXISTS information_technology_componentclassification;    
DROP TABLE IF EXISTS information_technology_deployment;                 
DROP TABLE IF EXISTS information_technology_process;                    
DROP TABLE IF EXISTS information_technology_process_classification;     
DROP TABLE IF EXISTS information_technology_processclassification;      
DROP TABLE IF EXISTS information_technology_processframework;           
DROP TABLE IF EXISTS job_management_job;                                
DROP TABLE IF EXISTS job_management_jobpartyrole;                       
DROP TABLE IF EXISTS job_management_jobpartyrole_email_contacts;        
DROP TABLE IF EXISTS job_management_jobpartyrole_logical_resources;     
DROP TABLE IF EXISTS job_management_jobpartyrole_physical_contacts;     
DROP TABLE IF EXISTS job_management_jobpartyrole_physical_resources;    
DROP TABLE IF EXISTS job_management_jobpartyrole_telephone_numbers;     
DROP TABLE IF EXISTS location_city;                                     
DROP TABLE IF EXISTS location_country;                                  
DROP TABLE IF EXISTS location_location;                                 
DROP TABLE IF EXISTS location_province;    
DROP TABLE IF EXISTS location_poboxaddress;                             
DROP TABLE IF EXISTS location_ruralpropertyaddress;                     
DROP TABLE IF EXISTS location_ruralpropertysubaddress;                  
DROP TABLE IF EXISTS location_urbanpropertyaddress;                     
DROP TABLE IF EXISTS location_urbanpropertysubaddress;                  
DROP TABLE IF EXISTS loyalty_loyaltyscheme;                             
DROP TABLE IF EXISTS loyalty_loyaltytransaction;                        
DROP TABLE IF EXISTS loyalty_loyaltytransaction_sale_items;             
DROP TABLE IF EXISTS market_marketsegment;                              
DROP TABLE IF EXISTS market_marketstrategy;                             
DROP TABLE IF EXISTS order_estimate;                                    
DROP TABLE IF EXISTS order_order;                                       
DROP TABLE IF EXISTS order_orderitem;                                   
DROP TABLE IF EXISTS order_quote;                                       
DROP TABLE IF EXISTS party_emailcontact;                                
DROP TABLE IF EXISTS party_genericpartyrole;                            
DROP TABLE IF EXISTS party_genericpartyrole_email_contacts;             
DROP TABLE IF EXISTS party_genericpartyrole_logical_resources;          
DROP TABLE IF EXISTS party_genericpartyrole_physical_contacts;          
DROP TABLE IF EXISTS party_genericpartyrole_physical_resources;         
DROP TABLE IF EXISTS party_genericpartyrole_telephone_numbers;          
DROP TABLE IF EXISTS party_individual;                                  
DROP TABLE IF EXISTS party_organisation;                                
DROP TABLE IF EXISTS party_owner;                                       
DROP TABLE IF EXISTS party_owner_email_contacts;                        
DROP TABLE IF EXISTS party_owner_logical_resources;                     
DROP TABLE IF EXISTS party_owner_physical_contacts;                     
DROP TABLE IF EXISTS party_owner_physical_resources;                    
DROP TABLE IF EXISTS party_owner_telephone_numbers;                     
DROP TABLE IF EXISTS party_partyroleassociation;                        
DROP TABLE IF EXISTS party_physicalcontact;                             
DROP TABLE IF EXISTS party_telephonenumber;                             
DROP TABLE IF EXISTS physical_object_device;                            
DROP TABLE IF EXISTS physical_object_structure;                         
DROP TABLE IF EXISTS physical_object_vehicle;                           
DROP TABLE IF EXISTS pricing_pricecalculation;                          
DROP TABLE IF EXISTS pricing_pricecalculation_accounts;                 
DROP TABLE IF EXISTS pricing_pricecalculation_categories;               
DROP TABLE IF EXISTS pricing_pricecalculation_customers;                
DROP TABLE IF EXISTS pricing_pricecalculation_product_offerings;        
DROP TABLE IF EXISTS pricing_pricecalculation_stores;                   
DROP TABLE IF EXISTS pricing_pricechannel;                              
DROP TABLE IF EXISTS pricing_productofferingprice;                      
DROP TABLE IF EXISTS pricing_productofferingprice_categories;           
DROP TABLE IF EXISTS pricing_promotion;                                 
DROP TABLE IF EXISTS pricing_promotion_categories;                      
DROP TABLE IF EXISTS pricing_promotion_customers;                       
DROP TABLE IF EXISTS pricing_promotion_product_offerings;               
DROP TABLE IF EXISTS pricing_promotion_stores;                          
DROP TABLE IF EXISTS product_product;                                   
DROP TABLE IF EXISTS product_product_bundle;                            
DROP TABLE IF EXISTS product_product_categories;                        
DROP TABLE IF EXISTS product_productassociation;                        
DROP TABLE IF EXISTS product_productcategory;                           
DROP TABLE IF EXISTS product_productoffering;                           
DROP TABLE IF EXISTS product_productoffering_channels;                  
DROP TABLE IF EXISTS product_productoffering_segments;                  
DROP TABLE IF EXISTS product_productoffering_strategies;                
DROP TABLE IF EXISTS product_productspecification;                      
DROP TABLE IF EXISTS product_productstock;                              
DROP TABLE IF EXISTS product_productstocktake;                          
DROP TABLE IF EXISTS product_supplierproduct;                           
DROP TABLE IF EXISTS project_project;                                   
DROP TABLE IF EXISTS project_project_components;                        
DROP TABLE IF EXISTS project_project_processes;                         
DROP TABLE IF EXISTS resource_logicalresource;                          
DROP TABLE IF EXISTS resource_physicalresource;                         
DROP TABLE IF EXISTS resource_physicalresource_physical_objects;        
DROP TABLE IF EXISTS resource_resourceorder;                            
DROP TABLE IF EXISTS resource_resourceorderitem;                        
DROP TABLE IF EXISTS sale_purchaser;                                    
DROP TABLE IF EXISTS sale_purchaser_email_contacts;                     
DROP TABLE IF EXISTS sale_purchaser_logical_resources;                  
DROP TABLE IF EXISTS sale_purchaser_physical_contacts;                  
DROP TABLE IF EXISTS sale_purchaser_physical_resources;                 
DROP TABLE IF EXISTS sale_purchaser_telephone_numbers;                  
DROP TABLE IF EXISTS sale_sale;                                         
DROP TABLE IF EXISTS sale_sale_credit_balance_events;                   
DROP TABLE IF EXISTS sale_saleitem;                                     
DROP TABLE IF EXISTS sale_saleschannel;                                 
DROP TABLE IF EXISTS sale_tender;                                       
DROP TABLE IF EXISTS sale_tendertype;                                   
DROP TABLE IF EXISTS store_store;                                       
DROP TABLE IF EXISTS store_store_email_contacts;                        
DROP TABLE IF EXISTS store_store_logical_resources;                     
DROP TABLE IF EXISTS store_store_physical_contacts;                     
DROP TABLE IF EXISTS store_store_physical_resources;                    
DROP TABLE IF EXISTS store_store_telephone_numbers;                     
DROP TABLE IF EXISTS supplier_partner_buyer;                            
DROP TABLE IF EXISTS supplier_partner_buyer_email_contacts;             
DROP TABLE IF EXISTS supplier_partner_buyer_logical_resources;          
DROP TABLE IF EXISTS supplier_partner_buyer_physical_contacts;          
DROP TABLE IF EXISTS supplier_partner_buyer_physical_resources;         
DROP TABLE IF EXISTS supplier_partner_buyer_telephone_numbers;          
DROP TABLE IF EXISTS supplier_partner_partner;                          
DROP TABLE IF EXISTS supplier_partner_partner_email_contacts;           
DROP TABLE IF EXISTS supplier_partner_partner_logical_resources;        
DROP TABLE IF EXISTS supplier_partner_partner_physical_contacts;        
DROP TABLE IF EXISTS supplier_partner_partner_physical_resources;       
DROP TABLE IF EXISTS supplier_partner_partner_telephone_numbers;        
DROP TABLE IF EXISTS supplier_partner_supplier;                         
DROP TABLE IF EXISTS supplier_partner_supplier_email_contacts;          
DROP TABLE IF EXISTS supplier_partner_supplier_logical_resources;       
DROP TABLE IF EXISTS supplier_partner_supplier_physical_contacts;       
DROP TABLE IF EXISTS supplier_partner_supplier_physical_resources;      
DROP TABLE IF EXISTS supplier_partner_supplier_telephone_numbers;       
DROP TABLE IF EXISTS supplier_partner_supplieraccount;                  
DROP TABLE IF EXISTS supply_chain_asns;                                 
DROP TABLE IF EXISTS supply_chain_poexpecteddeliverydate;               
DROP TABLE IF EXISTS supply_chain_purchaseorder;                        
DROP TABLE IF EXISTS supply_chain_purchaseorderacknowledgementlineitems;
DROP TABLE IF EXISTS supply_chain_purchaseorderacknowledgements;        
DROP TABLE IF EXISTS supply_chain_purchaseorderlineitems;               
DROP TABLE IF EXISTS supply_chain_schemaversion;                        
DROP TABLE IF EXISTS supply_chain_sscc;                                 
DROP TABLE IF EXISTS supply_chain_ssccauditcorrectionactions;           
DROP TABLE IF EXISTS supply_chain_ssccauditcorrectionproductitems;      
DROP TABLE IF EXISTS supply_chain_ssccauditcorrectionreversal;          
DROP TABLE IF EXISTS supply_chain_ssccauditcorrections;                 
DROP TABLE IF EXISTS supply_chain_ssccauditproductitems;                
DROP TABLE IF EXISTS supply_chain_ssccaudits;                           
DROP TABLE IF EXISTS supply_chain_ssccdelivery;                         
DROP TABLE IF EXISTS supply_chain_ssccgoodsreceipt;                     
DROP TABLE IF EXISTS supply_chain_ssccmandatoryauditcontrol;            
DROP TABLE IF EXISTS supply_chain_ssccproductitems;                     
DROP TABLE IF EXISTS supply_chain_synchronisations;                     
DROP TABLE IF EXISTS supply_chain_synchronisationsend;                  
DROP TABLE IF EXISTS supply_chain_unrecognisedsscc;                     
DROP TABLE IF EXISTS trouble_problem;                                   
DROP TABLE IF EXISTS trouble_problem_affected_locations;                
DROP TABLE IF EXISTS trouble_problem_affected_resources;                
DROP TABLE IF EXISTS trouble_problem_associated_trouble_tickets;        
DROP TABLE IF EXISTS trouble_problem_underlying_problems;               
DROP TABLE IF EXISTS trouble_resourcealarm;                             
DROP TABLE IF EXISTS trouble_trackingrecord;                            
DROP TABLE IF EXISTS trouble_troubleticket;                             
DROP TABLE IF EXISTS trouble_troubleticketitem;       
DROP TABLE IF EXISTS location_geographicarea;                  
DROP TABLE IF EXISTS store_store_buildings;                      
SET FOREIGN_KEY_CHECKS = 1;
