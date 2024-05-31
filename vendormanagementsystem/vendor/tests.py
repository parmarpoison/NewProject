from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PurchaseOrder, VendorPerformance

class TestVendorManagementSystem(TestCase):
    def setUp(self):
        self.client = APIClient()

    class TestVendorManagementSystem(TestCase):
        def setUp(self):
            self.client = APIClient()

    def test_create_vendor(self):
        data = {
            'name': 'New Vendor',
            'contact_details' : 'New Vendor Contact',
            'address' : 'New Vendor Address',
            'vendor_code' : 'New Vendor Code', 
            'on_time_delivery_rate' : 2,
            'quality_rating_avg' : 2,
            'average_response_time' : 2,
            'fulfillment_rate' : 2
        }
        response = self.client.post('/api/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_purchase_order(self):
        data = {
            'po_number': 'PO123',
            'vendor': 'Vendor Name',
            'order_date': '2024-05-10',
            'delivery_date': '2024-05-15',
            'items': ['Item1', 'Item2'],
            'quantity': [10, 20],
            'status': 'Pending',
            'issue_date': '2024-05-09'
        }
        response = self.client.post('/api/purchase_orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendor_performance(self):
        response = self.client.get('/api/vendors/1/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order(self):
        po = PurchaseOrder.objects.create(po_number='PO123', vendor='Vendor Name', order_date='2024-05-10', delivery_date='2024-05-15', items=['Item1', 'Item2'], quantity=[10, 20], status='Pending', issue_date='2024-05-09')
        response = self.client.post(f'/api/purchase_orders/{po.id}/acknowledge/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertIsNotNone(po.acknowledgment_date)

    def test_vendor_performance_update_on_po_completion(self):
        # Create a completed purchase order
        po = PurchaseOrder.objects.create(po_number='PO123', vendor='Vendor Name', order_date='2024-05-10', delivery_date='2024-05-15', items=['Item1', 'Item2'], quantity=[10, 20], status='Completed', issue_date='2024-05-09')
        # Ensure VendorPerformance is updated
        vendor_id = po.vendor.id
        initial_performance = VendorPerformance.objects.get(vendor_id=vendor_id)
        self.client.post(f'/api/purchase_orders/{po.id}/acknowledge/', {}, format='json')
        updated_performance = VendorPerformance.objects.get(vendor_id=vendor_id)
        self.assertNotEqual(initial_performance, updated_performance)
