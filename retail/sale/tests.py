from django.test import TestCase

from retail.sale.models import Sale, ImportDSR, dsr_sample

class SaleTestCase(TestCase):

    def test_bulk_dsr(self):
        """
        Make sure bulk imports of DSR files work
        """
        ImportDSR( "X1","30/05/2017",dsr_sample )
        self.assertTrue(len(Sale.objects.all())>0)
        
