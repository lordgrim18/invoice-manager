from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_valid_data_list = [
            {
                'customer_name': 'John Doe',
                'invoice_date': '2024-01-01T00:00:00Z',
                'invoice_details': [
                    {
                        'description': 'Product 1',
                        'quantity': 10,
                        'unit_price': 100,
                        'price': 1000
                    },
                    {
                        'description': 'Product 3',
                        'quantity': 2,
                        'unit_price': 200,
                    }
                ]
            },
            {
                'customer_name': 'Jane Doe',
                'invoice_details': [
                    {
                        'description': 'Product 2',
                        'quantity': 5,
                        'unit_price': 50,
                    },
                ]
            }
        ]

        self.invoice_invalid_data_list = [
            {
                'customer_name': 'John Doe',
                'invoice_date': 'invalid-date',
                'invoice_details': [
                    {
                        'description': 'Product 1',
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

    def test_create_invoice_success(self):
        Invoice.objects.all().delete()
        for count, invoice_valid_data in enumerate(self.invoice_valid_data_list, start=1):
            InvoiceDetail.objects.all().delete()
            response = self.client.post(
                reverse('invoice-create'), 
                invoice_valid_data, 
                )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Invoice.objects.count(), count)
            self.assertEqual(InvoiceDetail.objects.count(), len(invoice_valid_data['invoice_details']))
            self.assertEqual(response.data['message'], "successfully created new invoice")
            self.assertIn('data', response.data)

    def test_create_invoice_failure__empty(self):
        response = self.client.post(
            reverse('invoice-create'), 
            {}, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertIn('errors', response.data)

    def test_create_invoice_failure__no_customer_name(self):
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('customer_name')
        response = self.client.post(
            reverse('invoice-create'), 
            invoice_valid_data, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertEqual(response.data['errors']['customer_name'][0], "This field is required.")

    def test_create_invoice_failure__no_invoice_details(self):
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('invoice_details')
        response = self.client.post(
            reverse('invoice-create'), 
            invoice_valid_data, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to create new invoice")
        self.assertIn('errors', response.data)

    def test_create_invoice_failure__invalid_invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.post(
                reverse('invoice-create'), 
                invoice_invalid_data, 
                )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to create new invoice")
            self.assertIn('errors', response.data)

    def test_get_invoices_success(self):
        response = self.client.get(
            reverse('invoice-list')
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), Invoice.objects.count())
        self.assertEqual(response.data['results']['message'], "successfully retrieved invoices")

    def test_get_invoices_success__empty(self):
        Invoice.objects.all().delete()
        response = self.client.get(
            reverse('invoice-list')
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice_success(self):
        for invoice_valid_data in self.invoice_valid_data_list:
            response = self.client.put(
                reverse('invoice-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                        ), invoice_valid_data, 
                        )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "successfully updated invoice")
            self.assertIn('data', response.data)

    def test_update_invoice_failure__empty(self):
        response = self.client.put(
            reverse('invoice-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_update_invoice_failure__no_customer_name(self):
        invoice_valid_data = self.invoice_invalid_data_list[0]
        invoice_valid_data.pop('customer_name')
        response = self.client.put(
            reverse('invoice-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), invoice_valid_data, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertEqual(response.data['errors']['customer_name'][0], "This field is required.")

    def test_update_invoice_failure__no_invoice_details(self):
        invoice_valid_data = self.invoice_invalid_data_list[0]
        invoice_valid_data.pop('invoice_details')
        response = self.client.put(
            reverse('invoice-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), invoice_valid_data, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_update_invoice_failure__invalid_invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.put(
                reverse('invoice-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_invalid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice")
            self.assertIn('errors', response.data)

    def test_partial_update_invoice_success__name_date(self):
        for invoice_valid_data in self.invoice_valid_data_list:
            invoice_valid_data.pop('invoice_details')
            response = self.client.patch(
                reverse('invoice-partial-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_valid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "successfully updated invoice")
            self.assertIn('data', response.data)
    
    def test_partial_update_invoice_success__name(self):
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('invoice_details')
        invoice_valid_data.pop('invoice_date')
        response = self.client.patch(
            reverse('invoice-partial-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), invoice_valid_data, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)

    def test_partial_update_invoice_success__date(self):
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('invoice_details')
        invoice_valid_data.pop('customer_name')
        response = self.client.patch(
            reverse('invoice-partial-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), invoice_valid_data, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully updated invoice")
        self.assertIn('data', response.data)

    def test_partial_update_invoice_failure__empty(self):
        response = self.client.patch(
            reverse('invoice-partial-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice")
        self.assertIn('errors', response.data)

    def test_partial_update_invoice_failure__invoice_details(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.patch(
                reverse('invoice-partial-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_invalid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice")
            self.assertIn('errors', response.data)

    def test_delete_invoice_success(self):
        response = self.client.delete(
            reverse('invoice-delete',
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully deleted invoice")

    def test_delete_invoice_failure__invalid_id(self):
        response = self.client.delete(
            reverse('invoice-delete', 
                    kwargs={
                        'invoice_id': 'invalid_id'
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "invoice not found")

    def test_partial_update_invoice_detail_success(self):
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_detail_valid_data_list = invoice_valid_data.get('invoice_details')
        for invoice_detail_valid_data in invoice_detail_valid_data_list:
            response = self.client.patch(
                reverse('invoice-detail-partial-update', 
                        kwargs={
                            'invoice_detail_id': self.invoice_detail.id
                            }
                            ), invoice_detail_valid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "successfully updated invoice detail")

            for key, value in invoice_detail_valid_data.items():
                self.client.patch(
                    reverse('invoice-detail-partial-update', 
                            kwargs={
                                'invoice_detail_id': self.invoice_detail.id
                                }
                                ), {key: value}, 
                                )
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['message'], "successfully updated invoice detail")

    def test_partial_update_invoice_detail_failure__empty(self):
        response = self.client.patch(
            reverse('invoice-detail-partial-update', 
                    kwargs={
                        'invoice_detail_id': self.invoice_detail.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "failed to update invoice detail")
        self.assertIn('errors', response.data)

    def test_partial_update_invoice_detail_failure__invalid_invoice_detail(self):
        for invoice_invalid_data in self.invoice_invalid_data_list:
            invoice_detail_invalid_data = invoice_invalid_data.get('invoice_details')
            response = self.client.patch(
                reverse('invoice-detail-partial-update', 
                        kwargs={
                            'invoice_detail_id': self.invoice_detail.id
                            }
                            ), invoice_detail_invalid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['message'], "failed to update invoice detail")
            self.assertIn('errors', response.data)

    def test_delete_invoice_detail_success(self):
        response = self.client.delete(
            reverse('invoice-detail-delete', 
                    kwargs={
                        'invoice_detail_id': self.invoice_detail.id
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "successfully deleted invoice detail")

    def test_delete_invoice_detail_failure__invalid_id(self):
        response = self.client.delete(
            reverse('invoice-detail-delete', 
                    kwargs={
                        'invoice_detail_id': 'invalid_id'
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "invoice detail not found")