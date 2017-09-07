import datetime, os, random
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from cbe.party.models import Individual, Organisation, Owner, PartyRole
from cbe.location.models import Location
from cbe.customer.models import Customer, CustomerAccount
from cbe.resource.models import PhysicalResource
from cbe.human_resources.models import Staff, Identification, IdentificationType
from cbe.physical_object.models import Device
from cbe.credit.models import Credit, CreditBalanceEvent

from retail.store.models import Store
from retail.product.models import ProductOffering, Product
from retail.pricing.models import PriceChannel, PriceCalculation, Promotion, ProductOfferingPrice


class Purchaser(PartyRole):
    customer = models.ForeignKey(Customer, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, db_index=True, null=True,blank=True)
    credit = models.ForeignKey(Credit, null=True,blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "%s"%(self.party)

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = "Purchaser"          
        super(Purchaser, self).save(*args, **kwargs)
        

class SalesChannel(models.Model):
    name =  models.CharField(max_length=100 )

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s"%(self.name)


class Sale(models.Model):
    channel = models.ForeignKey(SalesChannel)
    store = models.ForeignKey(Store)
    seller = models.ForeignKey(Organisation)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    docket_number = models.CharField(max_length=50, null=True,blank=True )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_excl = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)

    purchaser = models.ForeignKey(Purchaser, db_index=True, null=True,blank=True)
    customer = models.ForeignKey(Customer, db_index=True, null=True,blank=True)
    account = models.ForeignKey(CustomerAccount, db_index=True, null=True,blank=True)
    identification = models.ForeignKey(Identification, null=True,blank=True )

    promotion = models.ForeignKey(Promotion, null=True,blank=True)
    till = models.ForeignKey(PhysicalResource, db_index=True, null=True,blank=True)
    staff = models.ForeignKey(Staff, db_index=True, null=True,blank=True)

    price_channel = models.ForeignKey(PriceChannel, null=True,blank=True)
    price_calculation = models.ForeignKey(PriceCalculation, null=True,blank=True)

    credit_balance_events = models.ManyToManyField(CreditBalanceEvent, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s|%s|%d"%(self.store,self.datetime,self.total_amount)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, db_index=True, related_name='sale_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, db_index=True, )
    product_offering = models.ForeignKey(ProductOffering, db_index=True, null=True,blank=True, )

    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('metre', 'metre')), default='each')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)

    promotion = models.ForeignKey(Promotion, null=True,blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return "%s"%self.product_offering


class TenderType(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Tender(models.Model):
    sale = models.ForeignKey(Sale, db_index=True, related_name='tenders', on_delete=models.CASCADE)
    tender_type = models.ForeignKey(TenderType)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return "%s %s"%(self.sale, self.tender_type)


def ImportDSR(storecode,datetxt,dsrdata,products={}): #DD/MM/YYYY
    from cbe.credit.models import CreditBalanceEvent
    
    cash, created = TenderType.objects.get_or_create(name="Cash")
    store_org, created = Organisation.objects.get_or_create( organisation_type="Store", name=storecode )
    store, created = Store.objects.get_or_create( name=storecode, code=storecode, organisation=store_org )
    org_type = ContentType.objects.get_for_model(Organisation)
    owner_role, created = Owner.objects.get_or_create( organisation=store_org )
    date = datetime.date(day=int(datetxt[0:2]),month=int(datetxt[3:5]),year=int(datetxt[6:10]))

    store_channel, created = SalesChannel.objects.get_or_create( name="Store" )
    internet_channel, created = SalesChannel.objects.get_or_create( name="Internet" )
    airpoints, created = IdentificationType.objects.get_or_create( name="Airpoints Card" )
    
    # TODO: 'Local' Product category if nat_retail & nat_cost = 0
    
    items = []
    tenders = []
    sales = []
    credit_events = []

    staff_list = {}
    for staff in Staff.objects.all():
        staff_list[staff.name] = staff
            
    promotions = {}
    for promotion in Promotion.objects.all():
        promotions[promotion.name] = promotion
        
    tills = {}
    for till in PhysicalResource.objects.filter( name="Till", owner=owner_role ):
        tills["%s:%s"%(till.owner,till.serial_number)] = till
        
    customer_accounts = {}
    for account in CustomerAccount.objects.all():
        customer_accounts[account.account_number] = account # account number = loyalty number or trade customer #

    ids = {}
    for id in Identification.objects.all():
        ids[id.number] = id
        
    for line in dsrdata:
        data = line.split(',')
        if data[0] == "1":
            time = datetime.time(int(data[25][1:3]),int(data[25][3:5]),0)
            date_time = timezone.make_aware(datetime.datetime.combine(date,time), timezone.get_current_timezone())
            #date_time = datetime.datetime.combine(date,time)
            docket_number = data[3].strip('"')
            sku = data[6].strip('"')
            product_name = data[7].strip('"')
            quantity = Decimal(data[9].strip('"'))
            amount_excl = Decimal(data[10].strip('"'))
            amount_tax = amount_excl*Decimal(0.15)
            amount_inc = amount_excl + amount_tax
            retail = Decimal(data[20].strip('"'))
            nat_retail = Decimal(data[31].strip('"'))
            nat_cost = Decimal(data[32].strip('"'))
            discount = (retail*quantity) - amount_inc
            cost = Decimal(data[32].strip('"'))
            tender_type = data[15].strip('"')
            barcode = data[16].strip('"')
            staff_code = data[26].strip('"')
            till_lineno = data[27].strip('"')
            till_type = data[28].strip('"')

            loyaltyno = data[17].strip('"')
            supplierid = data[18].strip('"')
            suppliersku = data[19].strip('"')
            local_retail_price = Decimal(data[20].strip('"'))
            stock_on_hand = Decimal(data[21].strip('"'))
            internet_flag = data[22].strip('"')
            trade_sale = data[23].strip('"')
            accountno = data[24].strip('"')
            calc_type = data[29].strip('"')
            calc_ref = data[30].strip('"')
            
            # Set the channel based on weather sale originated on web site
            if internet_flag != "":
                channel = internet_channel
            else:
                channel = store_channel
            
            # Get or create customer & account for trade or retail
            customer = None
            account = None
            if accountno not in ["","N","$"]:
                if accountno not in customer_accounts.keys():
                    customers = Customer.objects.filter( customer_number=accountno )
                    if len(customers) == 0:
                        customer = Customer( customer_number=accountno, managed_by=store_org, customer_status="new", valid_from=timezone.make_aware(datetime.datetime.now()) )
                        customer.organisation = Organisation.objects.create( name="Unknown" )
                        customer.save()
                    else:
                        customer = customers[0]
                    customer_accounts[accountno] = CustomerAccount.objects.create( account_number=accountno, account_status="new", customer=customer, managed_by=store_org )
                account = customer_accounts[accountno]
                customer = account.customer
            elif loyaltyno != "":
                if loyaltyno not in customer_accounts.keys():
                    customer = Customer( customer_number=loyaltyno, customer_status="new", valid_from=timezone.make_aware(datetime.datetime.now()) )
                    customer.individual = Individual.objects.create( name="Unknown" )
                    customer.save()
                    customer_accounts[loyaltyno] = CustomerAccount.objects.create( account_number=loyaltyno, account_status="new", customer=customer )
                account = customer_accounts[loyaltyno]
                customer = account.customer
              
            # Get or create identification if provided
            id = None
            if loyaltyno != "" and customer.party != None:
                if loyaltyno not in ids.keys():
                    ids[loyaltyno] = Identification( number=loyaltyno, identification_type=airpoints )
                    ids[loyaltyno].party  = customer.party
                    ids[loyaltyno].save()
                id = ids[loyaltyno]
            
            # Get or create till resource and corresponding device
            if "%s:%s"%(owner_role,till_lineno) not in tills.keys():
                device = Device( owner=owner_role, serial_number=till_lineno, physical_object_type="Till", model=till_type )
                device.save()
                tills["%s:%s"%(owner_role,till_lineno)] = PhysicalResource.objects.create( owner=owner_role, serial_number=till_lineno, name="Till" )
                tills["%s:%s"%(owner_role,till_lineno)].physical_objects.add(device)
            till = tills["%s:%s"%(owner_role,till_lineno)]
            
            # Create or get product
            if sku not in products:
                product = Product.objects.create(name=product_name, barcode=sku,status="active",)
                products[sku] = ProductOffering.objects.create(product=product, sku=sku, retail_price=retail)
            po = products[sku]
            po.channels.add(channel)

            # Create or get promotion
            promo_code = data[12].strip('"')
            promotion = None
            if promo_code != "":
                txt = data[13].strip('"')
                promo_start = datetime.date(day=int(txt[0:2]),month=int(txt[3:5]),year=int(txt[6:10]))
                txt = data[14].strip('"')
                promo_end = datetime.date(day=int(txt[0:2]),month=int(txt[3:5]),year=int(txt[6:10]))
                if promo_code not in promotions.keys():
                    promotions[promo_code] = Promotion.objects.create( name=promo_code, valid_from=promo_start, valid_to=promo_end)
                promotion = promotions[promo_code]
                promotion.stores.add(store_org)
                if customer != None:
                    promotion.customers.add(customer)
                promotion.product_offerings.add(po)

            # Add this price to the list of prices for the offering
            if( len(po.product_offering_prices.filter(amount=retail) ) == 0 ):
                pop = ProductOfferingPrice.objects.create( product_offering=po, amount=retail, promotion=promotion, name="Uncategorised price" )
                
            # Create or get staff
            if staff_code not in staff_list:
                person, created = Individual.objects.get_or_create(name=staff_code)
                staff_list[staff_code] = Staff.objects.create(name=staff_code, individual=person, company=store_org)
            staff = staff_list[staff_code]
                
            # Is the current line a new sale or another item for an existing sale
            if len(sales) == 0 or sales[-1].docket_number != docket_number:
                sale = Sale(    store=store,
                                seller=store_org,
                                datetime=date_time, 
                                docket_number=docket_number, 
                                total_amount=amount_inc, 
                                total_amount_excl=amount_excl, 
                                total_tax=amount_tax, 
                                staff=staff, 
                                total_discount=discount, 
                                promotion=promotion,
                                channel=channel,
                                customer=customer,
                                account=account,
                                identification=id,
                                till=till )
                sales.append(sale)

                if tender_type == "$":
                    tender = Tender(tender_type=cash, amount=amount_inc)
                    tender.tmpsale = sale
                    tenders.append( tender )
                elif account != None:
                    if account.credit_liabilities.count() > 0:
                        credit = account.credit_liabilities.first()
                    else:
                        credit = Credit( account=account, liability_ownership=store_org, customer=customer )
                    credit.credit_balance += amount_inc
                    credit.save()
                    credit_event = CreditBalanceEvent.objects.create(credit=credit,amount=amount_inc, balance = credit.credit_balance, customer=customer, account=account)
                    credit_event.tmpsale = sale
                    #sale.credit_balance_events.add( credit_event )
                    credit_events.append( credit_event )
                else:
                    print( "Unhandled tender type: %s. No tender or credit created"%tender_type)
            else:
                sale = sales[-1]
                sale.total_amount += amount_inc
                sale.total_amount_excl += amount_excl
                sale.total_tax += amount_tax
                sale.total_discount += discount
                if tender_type == "$":
                    tenders[-1].amount += amount_inc
                elif account != None:
                    credit_events[-1].amount += amount_inc
                    account.credit_balance += amount_inc
                    credit_events[-1].balance = account.credit_balance

            item = SaleItem(    amount=amount_excl, 
                                tax=amount_tax, 
                                product=po.product,
                                product_offering=po,
                                quantity=quantity, 
                                discount=discount, 
                                promotion=promotion)
            item.tmpsale=sale
            items.append(item)

    Sale.objects.bulk_create(sales)
    sales = {}
    for sale in Sale.objects.filter(store=store, seller=store_org, datetime__year=date.year, datetime__month=date.month, datetime__day=date.day,):
        sales[sale.docket_number] = sale

    for tender in tenders:
        tender.sale = sales[tender.tmpsale.docket_number]
    Tender.objects.bulk_create(tenders)

    #CreditBalanceEvent.objects.bulk_create(credit_events)
    for credit_event in credit_events:
        sales[credit_event.tmpsale.docket_number].credit_balance_events.add( credit_event )
    
    for item in items:
        item.sale = sales[item.tmpsale.docket_number]
    SaleItem.objects.bulk_create(items)

    for key, account in customer_accounts.items():
        if getattr(account, 'tmp_changed', False) == True:
            account.save()
    
    print("{}|{}|lines:{} | Sales:{} | Tenders:{} | Credit Sales:{} | Items:{}".format(storecode,datetxt,len(dsrdata),len(sales),len(tenders),len(credit_events),len(items)))
    
    return products

    
default_stores = [
    "X01", "X02","X03","X04","X05","X06","X07","X08","X09","X10", "X11","X12","X13","X14","X15","X16","X17","X18","X19","X20", "X21","X22","X23","X24","X25","X26","X27","X28","X29","X30", "X31","X32","X33","X34","X35","X36","X37","X38","X39","X40", "X41","X42","X43","X44","X45","X46","X47","X48","X49","X50",
    "X51","X52","X53","X54","X55","X56","X57","X58","X59","X60", "X61","X62","X63","X64","X65","X66","X67","X68","X69","X70", "X71","X72","X73","X74","X75","X76","X77","X78","X79","X80", "X81",
]
test5_stores = [
    "Fake Store 1","Fake Store 2","Fake Store 3","Fake Store 4","Fake Store 5",
]
test10_stores = test5_stores + [
    "Fake Store 6","Fake Store 7","Fake Store 8","Fake Store 9","Fake Store 10",
]

test20_stores = test10_stores + [
    "Fake Store 11","Fake Store 12","Fake Store 13","Fake Store 14","Fake Store 15","Fake Store 16","Fake Store 17","Fake Store 18","Fake Store 19","Fake Store 20",
]
test50_stores = test20_stores + [
    "Fake Store 21","Fake Store 22","Fake Store 23","Fake Store 24","Fake Store 25","Fake Store 26","Fake Store 27","Fake Store 28","Fake Store 29","Fake Store 30",
    "Fake Store 31","Fake Store 32","Fake Store 33","Fake Store 34","Fake Store 35","Fake Store 36","Fake Store 37","Fake Store 38","Fake Store 39","Fake Store 40",
    "Fake Store 41","Fake Store 42","Fake Store 43","Fake Store 44","Fake Store 45","Fake Store 46","Fake Store 47","Fake Store 48","Fake Store 49","Fake Store 50",
]

def fake(stores=test5_stores, day_count=2,year=2000,month=1,day=1,path = None):
    from django.db import connections
    from django.db.utils import DatabaseError
    from time import sleep
    
    start_date = datetime.date(day=day, month=month, year=year)

    print( "Indexing %d products"%ProductOffering.objects.count() )
    products = {}
    for offering in ProductOffering.objects.all():
        products[offering.sku] = offering
    
    if path != None:
        listdir = os.listdir(path)
    
        for date in (start_date + datetime.timedelta(n) for n in range(day_count)):
            for store in stores:
                try:
                    dsr = []
                    while len(dsr) < 5:
                        with open(path + random.choice(listdir)) as f:
                            dsr = f.readlines()
                    
                    done = False
                    while not done:
                        try:
                            products = ImportDSR(store, "{0:02d}/{1:02d}/{2:04d}".format(date.day,date.month,date.year), dsr, products)
                            done = True
                        except DatabaseError as err:
                            print( "DATABASE ERROR! Closing unusable connections and retrying shortly. %s"%err )
                            sleep(10)
                            for conn in connections.all():
                                conn.close_if_unusable_or_obsolete()
                            sleep(10)
                        
                except UnicodeDecodeError as err:
                    print( "ERROR: %s"%err )
    else:
        for date in (start_date + datetime.timedelta(n) for n in range(day_count)):
            for store in stores:
                products = ImportDSR(store, "{0:02d}/{1:02d}/{2:04d}".format(date.day,date.month,date.year), dsr_sample, products)
    
            
dsr_sample = """
0,"X18","30/11/2016"
1,"X18","30/11/2016","1","12","0824","243728","GAS CARTRIDGE BUTANE 220G 4 PACK NO. 8","","1","8.68","6.54","","","","$","9420047505794","1234567","MIMP","MFS-1A (RVR)",9.98,33,"","N","$","0725","ME",1,"RET","retail","",9.98,6.54
1,"X18","30/11/2016","2","14","3114","173502","SPRITE 600ML","","1","3.37","2.56","","","","$","9300675009867","","CCAL","5736",3.88,38,"","N","ZZBUCKLL","0649","ME",1,"RET","retail","",3.88,2.57
1,"X18","30/11/2016","3","14","3114","173500","LIFT PLUS 355ML","","1","2.92","1.99","","","","$","9300675014496","","CCAL","8684",3.36,60,"","N","ZZROSSER","0650","ME",1,"RET","retail","",3.36,2
1,"X18","30/11/2016","3","14","3114","224726","WAIWERA WATER STILL SIPPER 750ML","","1","1.25","0.89","","","","$","9418482000226","","WWTR","WW0750P1ST",1.69,49,"","N","ZZROSSER","0650","ME",2,"RET","matrix","ME",1.69,0.92
1,"X18","30/11/2016","4","03","2575","180837","NAILER IMPULSE FRAMEMASTER-LI PASLODE","P","1","695.65","721","DEPT 03","02/02/2012","31/12/2016","0","9315104015746","","PASL","B20543",800,0,"","T","CRMPLUMB","0741","KB",1,"RET","promo","DEPT 03",949,771.75
1,"X18","30/11/2016","5","33","2794","277084","AUGER BIT 45HSC     12MM JOBMATE","","1","11.29","3.78","","","","$","9420047514901","","ARCH","J810-9212",12.98,9,"","N","$","0713","ME",1,"RET","retail","",12.98,3.8
1,"L9", "30/11/2016","6","07","3680","232144","NO-FIL ROLL 120GRIT 115MM X 5M","","1","16.03","7.22","","","","$","9310357270669","2642083224119","SAIN","66623398237",18.44,4,"","N","$","0834","RA",1,"RET","retail","",18.47,7.23
1,"A3","30/11/2016","147","05","1590","234415","SCREW CAP STORM/W   90MM","","1","5.08","2.61","","","","0","9323714055687","2642083462658","MRLY","736C.90",6.49,2,"","C","M10-FARMLANDS","1142","MB",6,"RET","matrix","M10-FARMLANDSGR",6.49,2.61
1,"A3","30/11/2016","169","05","1595","159238","HANSEN LD 15MM BEND","","1","5.74","5.31","","","","0","9414940000944","","HANP","HB15",10.8,8,"","N","HANSON","1159","RH",2,"RET","matrix","STAFFD",10.29,5.31
9,FinishedEx
""".split('\n')