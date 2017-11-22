from django.test import TestCase

from retail.sale.models import Sale
from retail.sale.utils import ImportDSR, ImportDSRLine, dsr_sample, dsr_sale

class SaleTestCase(TestCase):

    def test_bulk_dsr(self):
        """
        Make sure bulk imports of DSR files work
        """
        ImportDSR( dsr_sample, "X1" )
        self.assertTrue(len(Sale.objects.all())>0)
        
    def test_single_dsr(self):
        """
        Make sure bulk imports of DSR files work
        """
        sale = ImportDSRLine(dsr_sale)
        self.assertTrue(len(Sale.objects.all())>0)

    def test_curl(self):
        """
        curl -X POST http://127.0.0.1/api/sale/sale/create_from_dsr/ -u <uname>:<pw> -H "Content-Type: text/plain" --data "@<filename>"
        """
        self.assertTrue(True)
        
