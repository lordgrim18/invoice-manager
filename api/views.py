from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .serializer import InvoiceSerializer, InvoiceDetailSerializer, MinimalInvoiceSerializer
from .models import Invoice, InvoiceDetail
from .utils import CustomResponse

class InvoiceAPIView(APIView):
    """
    API endpoint that allows invoices to be created and retrieved.
    The following methods have been implemented:

    - post  : create a new invoice
            : enter the the customer name, invoice date and entire invoice details in the request body
            : note that the entire invoice details must be entered
            : the invoice date will be automatically set to the current date if not entered in the request body

    - get   : retrieve all invoices
            : returns a list of all invoices which contains the customer name, invoice date and entire invoice details
            : the list can be filtered using the search and sort query parameters
            : search can be done using the customer name or invoice detail description 
            : sort can be done using the customer name, invoice date, description, price, quantity or unit price
            : the list is paginated and returns 10 items per page

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

class SingleInvoiceAPIView(APIView):
    """
    API endpoints that allows a single invoice to be retrieved.
    The following method has been implemented:

    - get : returns a single invoice containing the customer name, invoice date and entire invoice details by using the invoice id
          : is useful for retrieving a single invoice for viewing or updating
    
    - put    : update an existing invoice
             : enter the the customer name, invoice date and entire invoice details in the request body
             : note that the entire previous invoice details will be replaced with the new details
             : remember that invoice date has to be manually updated if required and doesn't happen automatically
             : this means that the invoice date will not be updated if it is not entered in the request body

    - patch  : update an existing invoice
             : enter the the customer name or invoice date or both in the request body
             : note that the previous entire invoice details will be retained and cannot be updated using this endpoint
             : remember that invoice date has to be manually updated if needed and doesn't happen automatically
             : this means that the invoice date will not be updated if it is not entered in the request body

    - delete : delete an existing invoice

    """
    def get(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse("invoice", "retrieval").not_found_response()
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice)
        return CustomResponse("invoice", "retrieval", data=serializer.data).success_response()
    
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

class InvoiceDetailAPIView(APIView):
    """
    API endpoints that allows invoice details to be retrieved and deleted.
    The following methods have been implemented:

    - patch  : update any aspect of an existing invoice detail
             : enter any of the description, quantity, unit price or price or all of them in the request body
             : to completely update an invoice and detail, use the invoice-update endpoint

    - delete : delete an existing invoice detail

    - post   : create a new invoice detail
             : enter the description, quantity, unit price and price if needed in the request body
             : note that the invoice id must be entered in the request body
             : this method is used to add new details to an existing invoice
             
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
    
    def post(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return CustomResponse(
                "invoice detail", 
                "creation"
                ).not_found_response(
                    message="invoice object not found - invalid invoice id"
                )
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceDetailSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(invoice=invoice)
            return CustomResponse("invoice detail", "creation", data=serializer.data).created_response()
        return CustomResponse("invoice detail", "creation", data=serializer.errors).failure_response()