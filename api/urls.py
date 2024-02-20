from django.urls import path
from .views import InvoiceAPIView

urlpatterns = [
    path('invoice/create/', InvoiceAPIView.as_view(), name='invoice-create'), #post
    path('invoice/', InvoiceAPIView.as_view(), name='invoice-list'), #get
    path('invoice/update/<str:invoice_id>/', InvoiceAPIView.as_view(), name='invoice-update'), #put
]