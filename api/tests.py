from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Invoice, InvoiceDetail

class InvoiceAPITest(APITestCase):
    """
    Test cases for Invoice API endpoints using Django REST framework.
    """
    def setUp(self):
        """
        Sets up test data for invoices and invoice details.

        Attributes:
        invoice_valid_data_list (list): List of valid data for creation and updation of invoices.
        invoice_invalid_data_list (list): List of invalid data causing errors.
        invoice (Invoice): A sample invoice object for testing.
        invoice_detail (InvoiceDetail): A sample invoice detail object for testing.
        """
        self.invoice_valid_data_list = [
            {
                'customer_name': 'John Doe',
                'invoice_date': '2024-01-01',
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
            customer_name='New Customer',
            invoice_date='2000-03-11'
        )
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='New Product',
            quantity=10,
            unit_price=100,
            price=1000
        )

class CreateInvoiceTests(InvoiceAPITest):
    """
    Test cases for creating invoices.
    """
    def setUp(self):
        super().setUp()
        Invoice.objects.all().delete()

    def test_create_invoice_success(self):
        """
        Tests successful invoice creation with valid data.
        """
        # Invoice.objects.all().delete()
        for count, invoice_valid_data in enumerate(self.invoice_valid_data_list, start=1):
            InvoiceDetail.objects.all().delete()
            response = self.client.post(
                reverse('invoice-create'), 
                invoice_valid_data, 
                )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Invoice.objects.count(), count)
            self.assertEqual(InvoiceDetail.objects.count(), len(invoice_valid_data['invoice_details']))

    def test_create_invoice_failure__empty(self):
        """
        Test failed invoice creation because of empty data.
        """
        response = self.client.post(
            reverse('invoice-create'), 
            {}, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_failure__no_customer_name(self):
        """
        Test failed invoice creation because of no customer name.
        """
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('customer_name')
        response = self.client.post(
            reverse('invoice-create'), 
            invoice_valid_data, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_failure__no_invoice_details(self):
        """
        Test failed invoice creation because of no invoice details.
        """
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_valid_data.pop('invoice_details')
        response = self.client.post(
            reverse('invoice-create'), 
            invoice_valid_data, 
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_failure__invalid_invoice_details(self):
        """
        Test failed invoice creation because of invalid invoice details.
        """
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.post(
                reverse('invoice-create'), 
                invoice_invalid_data, 
                )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class InvoiceListAPITests(InvoiceAPITest):
    """
    Test cases for Invoice API endpoints using Django REST framework.
    """

    def test_get_invoices_success(self):
        """
        Test successful retrieval of invoices.
        """
        response = self.client.get(
            reverse('invoice-list')
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), Invoice.objects.count())

    def test_get_invoices_success__empty(self):
        """
        Test successful retrieval of invoices when there are no invoices.
        """
        Invoice.objects.all().delete()
        response = self.client.get(
            reverse('invoice-list')
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class InvoiceUpdateTests(InvoiceAPITest):
    """
    Test cases for updating invoices using Django REST framework.
    """
    def test_update_invoice_success(self):
        """
        Test successful invoice updation with valid data.
        """
        for invoice_valid_data in self.invoice_valid_data_list:
            response = self.client.put(
                reverse('invoice-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                        ), invoice_valid_data, 
                        )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice_failure__empty(self):
        """
        Test failed invoice updation because of empty data.
        """
        response = self.client.put(
            reverse('invoice-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_failure__no_customer_name(self):
        """
        Test failed invoice updation because of no customer name.
        """
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

    def test_update_invoice_failure__no_invoice_details(self):
        """
        Test failed invoice updation because of no invoice details.
        """
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

    def test_update_invoice_failure__invalid_invoice_details(self):
        """
        Test failed invoice updation because of invalid invoice details.
        """
        for invoice_invalid_data in self.invoice_invalid_data_list:
            response = self.client.put(
                reverse('invoice-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_invalid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class InvoicePartialUpdateTests(InvoiceAPITest):
    """
    Test cases for partial update of invoices using Django REST framework.
    """

    def test_partial_update_invoice_success__name_date(self):
        """
        Test successful partial invoice updation with customer name and invoice date.
        """
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
    
    def test_partial_update_invoice_success__name(self):
        """
        Test successful partial invoice updation with customer name only.
        """
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

    def test_partial_update_invoice_success__date(self):
        """
        Test successful partial invoice updation with invoice date only.
        """
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

    def test_partial_update_invoice_failure__empty(self):
        """
        Test failed partial invoice updation because of empty data.
        """
        response = self.client.patch(
            reverse('invoice-partial-update', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_invoice_failure__invoice_details(self):
        """
        Test failed partial invoice updation because of sending invoice details in request body.
        """
        for invoice_valid_data in self.invoice_valid_data_list:
            response = self.client.patch(
                reverse('invoice-partial-update', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_valid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class InvoiceDeleteTests(InvoiceAPITest):
    """
    Test cases for deletion of invoices using Django REST framework.
    """

    def test_delete_invoice_success(self):
        """
        Test successful deletion of an invoice.
        """
        response = self.client.delete(
            reverse('invoice-delete',
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_invoice_failure__invalid_id(self):
        """
        Test failed deletion of an invoice because of invalid invoice id.
        """
        response = self.client.delete(
            reverse('invoice-delete', 
                    kwargs={
                        'invoice_id': 'invalid_id'
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SingleInvoiceAPITests(InvoiceAPITest):
    """
    Test cases for single invoice API endpoints using Django REST framework.
    """

    def test_get_single_invoice_success(self):
        """
        Test successful retrieval of a single invoice.
        """
        response = self.client.get(
            reverse('single-invoice', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invoice_failure__invalid_id(self):
        """
        Test failed retrieval of a single invoice because of invalid invoice id.
        """
        response = self.client.get(
            reverse('single-invoice', 
                    kwargs={
                        'invoice_id': 'invalid_id'
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class InvoiceDetailPartialUpdateTests(InvoiceAPITest):
    """
    Test cases for partial update of invoice details using Django REST framework.
    """

    def test_partial_update_invoice_detail_success(self):
        """
        Test successful partial update of an invoice detail.
        """
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

            for key, value in invoice_detail_valid_data.items():
                self.client.patch(
                    reverse('invoice-detail-partial-update', 
                            kwargs={
                                'invoice_detail_id': self.invoice_detail.id
                                }
                                ), {key: value}, 
                                )
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_invoice_detail_failure__empty(self):
        """
        Test failed partial update of an invoice detail because of empty data.
        """
        response = self.client.patch(
            reverse('invoice-detail-partial-update', 
                    kwargs={
                        'invoice_detail_id': self.invoice_detail.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_invoice_detail_failure__invalid_invoice_detail(self):
        """
        Test failed partial update of an invoice detail because of invalid data.
        """
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

class InvoiceDetailDeleteTests(InvoiceAPITest):
    """
    Test cases for deletion of invoice details using Django REST framework.
    """

    def test_delete_invoice_detail_success(self):
        """
        Test successful deletion of an invoice detail.
        """
        response = self.client.delete(
            reverse('invoice-detail-delete', 
                    kwargs={
                        'invoice_detail_id': self.invoice_detail.id
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_invoice_detail_failure__invalid_id(self):
        """
        Test failed deletion of an invoice detail because of invalid invoice detail id.
        """
        response = self.client.delete(
            reverse('invoice-detail-delete', 
                    kwargs={
                        'invoice_detail_id': 'invalid_id'
                        }
                        ))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class InvoiceDetailCreateTests(InvoiceAPITest):
    """
    Test cases for creation of invoice details using Django REST framework.
    """

    def test_create_invoice_detail_success(self):
        """
        Test successful creation of an invoice detail.
        """
        invoice_valid_data = self.invoice_valid_data_list[0]
        invoice_detail_valid_data_list = invoice_valid_data.get('invoice_details')
        for invoice_detail_valid_data in invoice_detail_valid_data_list:
            response = self.client.post(
                reverse('invoice-detail-create', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_detail_valid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invoice_detail_failure__empty(self):
        """
        Test failed creation of an invoice detail because of empty data.
        """
        response = self.client.post(
            reverse('invoice-detail-create', 
                    kwargs={
                        'invoice_id': self.invoice.id
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_detail_failure__invalid_invoice_detail(self):
        """
        Test failed creation of an invoice detail because of invalid data.
        """
        for invoice_invalid_data in self.invoice_invalid_data_list:
            invoice_detail_invalid_data = invoice_invalid_data.get('invoice_details')
            response = self.client.post(
                reverse('invoice-detail-create', 
                        kwargs={
                            'invoice_id': self.invoice.id
                            }
                            ), invoice_detail_invalid_data, 
                            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_detail_failure__invalid_invoice_id(self):
        """
        Test failed creation of an invoice detail because of invalid invoice id.
        """
        response = self.client.post(
            reverse('invoice-detail-create', 
                    kwargs={
                        'invoice_id': 'invalid_id'
                        }
                        ), {}, 
                        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class InvoicePaginationTests(APITestCase):
    """
    Test cases for pagination of invoices.
    """
    
    def setUp(self):
        Invoice.objects.bulk_create(
            [Invoice(customer_name=f"Customer {i}", invoice_date=f"2023-02-{23-i}") for i in range(1, 16)]
        )

    def test_pagination(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]["data"]), 10)
        self.assertIn(reverse('invoice-list') + "?page=2", response.data["next"])
        self.assertEqual(response.data["previous"], None)

        response = self.client.get(reverse('invoice-list') + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]["data"]), 5)
        self.assertEqual(response.data["next"], None)
        self.assertIn(reverse('invoice-list'), response.data["previous"])

        self.assertEqual(response.data["count"], 15)

class InvoicePaginationSearchTests(APITestCase):

    def setUp(self):
        Invoice.objects.create(customer_name="Alice", invoice_date="2023-02-22")
        Invoice.objects.create(customer_name="Bob", invoice_date="2023-02-21")
        InvoiceDetail.objects.create(
            invoice=Invoice.objects.get(customer_name="Alice"), description="Laptop", quantity=1, unit_price=1000, price=1000
        )

    def test_search_by_customer_name(self):
        response = self.client.get(reverse('invoice-list') + "?search=Alice")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"].get("data")), 1)
        self.assertEqual(response.data['results']['data'][0]['customer_name'], "Alice")

    def test_search_by_invoice_detail_description(self):
        response = self.client.get(reverse('invoice-list') + "?search=Laptop")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"].get("data")), 1)
        self.assertEqual(
            response.data['results']['data'][0]['invoice_details'][0]['description'], "Laptop"
        )
    
    def test_search_no_results(self):
        response = self.client.get(reverse('invoice-list') + "?search=foobar")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"].get("data")), 0)

class InvoicePaginationSortTests(APITestCase):

    def setUp(self):
        invoices = [
            Invoice.objects.create(
                customer_name=f"Customer {i}", invoice_date=f"2023-02-{23-i}"
            )
            for i in range(1, 5)
        ]
        for index, invoice in enumerate(invoices, start=1):
            InvoiceDetail.objects.create(invoice=invoice, quantity=index, unit_price=index*10, price=index*10*index) 

    def test_sort_by_customer_name_asc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=customer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["customer_name"] for d in response.data["results"]["data"]],
            ["Customer 1", "Customer 2", "Customer 3", "Customer 4"],
        )

    def test_sort_by_customer_name_desc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=-customer")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["customer_name"] for d in response.data["results"]["data"]],
            ["Customer 4", "Customer 3", "Customer 2", "Customer 1"],
        )

    def test_sort_by_date_asc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=date")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_date"] for d in response.data["results"]["data"]],
            ['2023-02-19', '2023-02-20', '2023-02-21', '2023-02-22'],
        )
    
    def test_sort_by_date_desc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=-date")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_date"] for d in response.data["results"]["data"]],
            ['2023-02-22', '2023-02-21', '2023-02-20', '2023-02-19'],
        )

    def test_sort_by_invoice_detail_quantity_asc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=quantity")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_details"][0]["quantity"] for d in response.data["results"]["data"]],
            [1, 2, 3, 4],
        )

    def test_sort_by_invoice_detail_quantity_desc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=-quantity")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_details"][0]["quantity"] for d in response.data["results"]["data"]],
            [4, 3, 2, 1],
        )

    def test_sort_by_invoice_detail_price_asc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=price")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_details"][0]["price"] for d in response.data["results"]["data"]],
            [10, 40, 90, 160],
        )
    
    def test_sort_by_invoice_detail_price_desc(self):
        response = self.client.get(reverse('invoice-list') + "?sort=-price")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [d["invoice_details"][0]["price"] for d in response.data["results"]["data"]],
            [160, 90, 40, 10],
        )