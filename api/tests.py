from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Invoice, InvoiceDetail

class InvoiceCreateAPITest(APITestCase):
    def setUp(self):
        self.invoice_valid_data = {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': 100,
                    'price': 1000
                },
                {
                    'description': 'Product 2',
                    'quantity': 5,
                    'unit_price': 50,
                    'price': 250
                },
                {
                    'description': 'Product 3',
                    'quantity': 2,
                    'unit_price': 200
                }
            ]
        }

        self.invoice_invalid_data_list = [
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'quantity': 10,
                    'unit_price': 100,
                    'price': 1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'unit_price': 100,
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': 100,
                    'price': -1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': -10,
                    'unit_price': 100,
                    'price': 1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': -100,
                    'price': 1000
                },
            ]
            }
        ]

    def test_create_invoice_success(self):
        response = self.client.post(reverse('invoice-create'), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), len(self.invoice_valid_data['invoice_details']))
        self.assertEqual(response.data['message'], "successfully created new invoice")
        self.assertIn('data', response.data)

    def test_create_invoice_failure__empty(self):
        response = self.client.post(reverse('invoice-create'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertIn('errors', response.data)

    def test_create_invoice_failure__no_customer_name(self):
        self.invoice_valid_data.pop('customer_name')
        response = self.client.post(reverse('invoice-create'), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertEqual(response.data['errors']['customer_name'][0], "This field is required.")

    def test_create_invoice_failure__no_invoice_details(self):
        self.invoice_valid_data.pop('invoice_details')
        response = self.client.post(reverse('invoice-create'), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertIn('errors', response.data)

    def test_create_invoice_failure__invalid_invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.post(reverse('invoice-create'), invoice_invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to create new invoice")
            self.assertIn('errors', response.data)

class InvoiceListAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail_1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )
        self.invoice_detail_2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 2',
            quantity=5,
            unit_price=50,
            price=250
        )
        self.invoice_detail_3 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 3',
            quantity=2,
            unit_price=200,
            price=400
        )

    def test_get_invoices_success(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), Invoice.objects.count())
        self.assertEqual(response.data['message'], "successfully retrieved invoices")
        self.assertIn('data', response.data)

    def test_get_invoices_success__empty(self):
        Invoice.objects.all().delete()
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully retrieved invoices")
        self.assertEqual(response.data['data'], [])

class InvoiceUpdateAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail_1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )
        self.invoice_detail_2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 2',
            quantity=5,
            unit_price=50,
            price=250
        )
        self.invoice_detail_3 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 3',
            quantity=2,
            unit_price=200,
            price=400
        )

        self.invoice_valid_data = {
            'customer_name': 'John Doe',
            'invoice_date': '2021-01-01T00:00:00Z', 
            'invoice_details': [
                {
                    'description': 'Product 4',
                    'quantity': 16,
                    'unit_price': 166,
                    'price': 2656
                },
                {
                    'description': 'Product 5',
                    'quantity': 7,
                    'unit_price': 10,
                    'price': 70
                },
            ]
        }

        self.invoice_invalid_data_list = [
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'quantity': 10,
                    'unit_price': 100,
                    'price': 1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'unit_price': 100,
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': 100,
                    'price': -1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': -10,
                    'unit_price': 100,
                    'price': 1000
                },
            ]
            },
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': -100,
                    'price': 1000
                },
            ]
            }
        ]

    def test_update_invoice_success(self):
        response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)

    def test_update_invoice_failure__empty(self):
        response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': self.invoice.id}), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_update_invoice_failure__no_customer_name(self):
        self.invoice_valid_data.pop('customer_name')
        response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertEqual(response.data['errors']['customer_name'][0], "This field is required.")

    def test_update_invoice_failure__no_invoice_details(self):
        self.invoice_valid_data.pop('invoice_details')
        response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_update_invoice_failure__invalid_invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.put(reverse('invoice-update', kwargs={'invoice_id': self.invoice.id}), invoice_invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice")
            self.assertIn('errors', response.data)

class InvoicePartialUpdateAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail_1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )
        self.invoice_detail_2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 2',
            quantity=5,
            unit_price=50,
            price=250
        )
        self.invoice_detail_3 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 3',
            quantity=2,
            unit_price=200,
            price=400
        )

        self.invoice_valid_data = {
            'customer_name': 'John Doe',
            'invoice_date': '2021-01-01T00:00:00Z',
        }

        self.invoice_invalid_data_list = [
            {
            'customer_name': 'John Doe',
            'invoice_details': [
                {
                    'description': 'Product 1',
                    'quantity': 10,
                    'unit_price': 100,
                    'price': 1000
                },
            ]
            },
        ]

    def test_partial_update_invoice_success__name_date(self):
        response = self.client.patch(reverse('invoice-partial-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)
    
    def test_partial_update_invoice_success__name(self):
        self.invoice_valid_data.pop('invoice_date')
        response = self.client.patch(reverse('invoice-partial-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)

    def test_partial_update_invoice_success__date(self):
        self.invoice_valid_data.pop('customer_name')
        response = self.client.patch(reverse('invoice-partial-update', kwargs={'invoice_id': self.invoice.id}), self.invoice_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)

    def test_partial_update_invoice_failure__empty(self):
        response = self.client.patch(reverse('invoice-partial-update', kwargs={'invoice_id': self.invoice.id}), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_partial_update_invoice_failure__invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.patch(reverse('invoice-partial-update', kwargs={'invoice_id': self.invoice.id}), invoice_invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice")
            self.assertIn('errors', response.data)

class InvoiceDeleteAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail_1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )
        self.invoice_detail_2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 2',
            quantity=5,
            unit_price=50,
            price=250
        )
        self.invoice_detail_3 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 3',
            quantity=2,
            unit_price=200,
            price=400
        )

    def test_delete_invoice_success(self):
        response = self.client.delete(reverse('invoice-delete', kwargs={'invoice_id': self.invoice.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully deleted invoice")

    def test_delete_invoice_failure__invalid_id(self):
        response = self.client.delete(reverse('invoice-delete', kwargs={'invoice_id': 'invalid_id'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "invoice not found")

class InvoiceDetailPartialUpdateAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )

        self.invoice_detail_valid_data = {
            'description': 'Product 2',
            'quantity': 20,
            'unit_price': 300,
            'price': 6000
        }

        self.invoice_detail_invalid_data_list = [
            {
            'description': 'Product 1',
            'quantity': 10,
            'unit_price': 100,
            'price': -1000
            },
            {
            'description': 'Product 1',
            'quantity': -10,
            'unit_price': 100,
            'price': 1000
            },
            {
            'description': 'Product 1',
            'quantity': 10,
            'unit_price': -100,
            'price': 1000
            }
        ]

    def test_partial_update_invoice_detail_success(self):
        response = self.client.patch(reverse('invoice-detail-partial-update', kwargs={'invoice_detail_id': self.invoice_detail.id}), self.invoice_detail_valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice detail")

        for key, value in self.invoice_detail_valid_data.items():
            self.client.patch(reverse('invoice-detail-partial-update', kwargs={'invoice_detail_id': self.invoice_detail.id}), {key: value}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "successfully updated invoice detail")

    def test_partial_update_invoice_detail_failure__empty(self):
        response = self.client.patch(reverse('invoice-detail-partial-update', kwargs={'invoice_detail_id': self.invoice_detail.id}), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice detail")
        self.assertIn('errors', response.data)

    def test_partial_update_invoice_detail_failure__invalid_invoice_detail(self):
        for invoice_detail_invalid_data in self.invoice_detail_invalid_data_list:
            response = self.client.patch(reverse('invoice-detail-partial-update', kwargs={'invoice_detail_id': self.invoice_detail.id}), invoice_detail_invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice detail")
            self.assertIn('errors', response.data)

class InvoiceDetailDeleteAPITest(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            customer_name='John Doe',\
            invoice_date='2021-01-01T00:00:00Z'
        )
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product 1',
            quantity=10,
            unit_price=100,
            price=1000
        )

    def test_delete_invoice_detail_success(self):
        response = self.client.delete(reverse('invoice-detail-delete', kwargs={'invoice_detail_id': self.invoice_detail.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully deleted invoice detail")

    def test_delete_invoice_detail_failure__invalid_id(self):
        response = self.client.delete(reverse('invoice-detail-delete', kwargs={'invoice_detail_id': 'invalid_id'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "invoice detail not found")