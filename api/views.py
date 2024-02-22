from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .serializer import InvoiceSerializer, InvoiceDetailSerializer
from .models import Invoice, InvoiceDetail
from .utils import CustomResponse

class InvoiceAPIView(APIView):
    """
    API endpoints that allows invoices to be created, retrieved, updated and deleted.
    The following methods have been implemented:

    - post  : create a new invoice
            : enter the the customer name, invoice date and entire invoice details in the request body
            : note that the entire invoice details must be entered
            : the invoice date will be automatically set to the current date if not entered in the request body

    - get   : retrieve all invoices
            : returns a list of all invoices which includes the customer name, invoice date and entire invoice details
            : the list can be filtered using the search query parameter
            : the list can be sorted using the sort query parameter
            : the list is paginated and returns 10 items per page

    - put   : update an existing invoice
            : enter the the customer name, invoice date and entire invoice details in the request body
            : note that the entire previous invoice details will be replaced with the new details
            : remember that invoice date has to be manually updated if required and doesn't happen automatically
            : this means that the invoice date will not be updated if it is not entered in the request body

    - patch : update an existing invoice
            : enter the the customer name or invoice date in the request body
            : note that the previous entire invoice details will be retained and cannot be updated using this endpoint
            : remember that invoice date has to be manually updated if needed and doesn't happen automatically
            : this means that the invoice date will not be updated if it is not entered in the request body

    - delete: delete an existing invoice

    """
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse("invoice", "creation", data=serializer.data).created_response()
        return CustomResponse("invoice", "creation", data=serializer.errors).failure_response()
    
    def get(self, request):
        invoices = Invoice.objects.all().prefetch_related('invoice_details')
        search_query = request.query_params.get('search', None)
        if search_query:
            invoices = invoices.filter(
                Q(customer_name__icontains=search_query) | 
                Q (invoice_details__description__icontains=search_query)
                   ).distinct().prefetch_related('invoice_details')
            
        sort_by_fields = {
            "customer": "customer_name",
            "date": "invoice_date",
            "description": "invoice_details__description",
            "price": "invoice_details__price",
            "quantity": "invoice_details__quantity",
            "unit_price": "invoice_details__unit_price"
        }
        sort_by = request.query_params.get('sort')
        if sort_by:
            if sort_by.startswith("-"):
                sort_by = f"-{sort_by_fields.get(sort_by[1:], 'invoice_date')}"
            else:
                sort_by = sort_by_fields.get(sort_by, '-invoice_date')
            invoices = invoices.order_by(sort_by)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(invoices, request)

        serializer = InvoiceSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response({
            "message": "successfully retrieved invoices",
            "data": serializer.data
            })
    
    def put(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse("invoice", "update").not_found_response()
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse("invoice", "update", data=serializer.data).success_response()
        return CustomResponse("invoice", "update", data=serializer.errors).failure_response()
    
    def patch(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse("invoice", "update").not_found_response()
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse("invoice", "update", data=serializer.data).success_response()
        return CustomResponse("invoice", "update", data=serializer.errors).failure_response()
    
    def delete(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse("invoice", "deletion").not_found_response()
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.delete()
        return CustomResponse("invoice", "deletion").success_response()
    
class SingleInvoiceAPIView(APIView):
    """
    API endpoints that allows a single invoice to be retrieved.
    The following method has been implemented:

    - get : retrieve a single invoice
          : returns a single invoice which includes the customer name, invoice date and entire invoice details
          : this method is used to retrieve a single invoice using the invoice id
          : is useful for retrieving a single invoice for viewing or updating
    """
    def get(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse("invoice", "retrieval").not_found_response()
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice)
        return CustomResponse("invoice", "retrieval", data=serializer.data).success_response()
    
class InvoiceDetailAPIView(APIView):
    """
    API endpoints that allows invoice details to be retrieved and deleted.
    The following methods have been implemented:

    - patch  : update any aspect existing invoice detail
             : enter any of the description, quantity, unit price or price in the request body
             : to completely update an invoice detail, use the invoice endpoint

    - delete : delete an existing invoice detail

    """
    def patch(self, request, invoice_detail_id):
        if not InvoiceDetail.objects.filter(id=invoice_detail_id).exists():
            return CustomResponse("invoice detail", "update").not_found_response()
        
        invoice_detail = InvoiceDetail.objects.get(id=invoice_detail_id)
        serializer = InvoiceDetailSerializer(invoice_detail, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse("invoice detail", "update", data=serializer.data).success_response()
        return CustomResponse("invoice detail", "update", data=serializer.errors).failure_response()

    def delete(self, request, invoice_detail_id):
        if not InvoiceDetail.objects.filter(id=invoice_detail_id).exists():
            return CustomResponse("invoice detail", "deletion").not_found_response()
        invoice_detail = InvoiceDetail.objects.get(id=invoice_detail_id)
        invoice_detail.delete()
        return CustomResponse("invoice detail", "deletion").success_response()