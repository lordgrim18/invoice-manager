from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import InvoiceSerializer
from .models import Invoice

class InvoiceAPIView(APIView):

    def post(self, request):
        invoice_details = request.data.pop('invoice_details', [])
        for detail in invoice_details:
            if 'price' not in detail:
                detail['price'] = float(float(detail['quantity']) * float(detail['unit_price']))
        request.data['invoice_details'] = invoice_details

        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "successfully created new invoice", 
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "failed to create new invoice", 
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(
            {
                "message": "successfully retrieved invoices", 
                "data": serializer.data
            }, status=status.HTTP_200_OK)
    
    def put(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return Response(
                {
                    "message": "invoice not found", 
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "successfully updated invoice", 
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
        return Response(
            {
                "message": "failed to update invoice", 
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, invoice_id):
        if not Invoice.objects.filter(id=invoice_id).exists():
            return Response(
                {
                    "message": "invoice not found", 
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.delete()
        return Response(
            {
                "message": "successfully deleted invoice", 
                "data": None
            }, status=status.HTTP_204_NO_CONTENT)