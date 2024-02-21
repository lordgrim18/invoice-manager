from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime

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
        self.assertEqual(response.data['errors'], "invoice details are required")

    def test_create_invoice_failure__invalid_invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.post(reverse('invoice-create'), invoice_invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to create new invoice")
            self.assertIn('errors', response.data)
