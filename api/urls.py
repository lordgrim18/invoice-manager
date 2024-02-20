from django.urls import path
from .views import InvoiceAPIView

urlpatterns = [
    path('invoice/create/', InvoiceAPIView.as_view(), name='invoice-create'),
]