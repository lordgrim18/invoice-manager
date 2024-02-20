from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import InvoiceSerializer

class InvoiceAPIView(APIView):

    def post(self, request):
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