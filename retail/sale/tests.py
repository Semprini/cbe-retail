from django.test import TestCase

from retail.sale.models import Sale
from retail.sale.utils import ImportDSR, ImportDSRLine, dsr_sample, dsr_sale

class SaleTestCase(TestCase):

    def test_bulk_dsr(self):
        """
        Make sure bulk imports of DSR files work
        """
        ImportDSR( "X1",dsr_sample.split('\n') )
        self.assertTrue(len(Sale.objects.all())>0)
        
    def test_single_dsr(self):
        """
        Make sure bulk imports of DSR files work
        """
        sale = ImportDSRLine(dsr_sale)
        self.assertTrue(len(Sale.objects.all())>0)
