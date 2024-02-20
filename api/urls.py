from django.urls import path
from .views import InvoiceAPIView, SingleInvoiceAPIView, InvoiceDetailAPIView

urlpatterns = [
    path(
        'invoice/create/', 
        InvoiceAPIView.as_view(), 
        name='invoice-create'
        ), #post
    path(
        'invoice/', 
        InvoiceAPIView.as_view(), 
        name='invoice-list'
        ), #get list
    path(
        'invoice/update/<str:invoice_id>/', 
        InvoiceAPIView.as_view(), 
        name='invoice-update'
        ), #put
    path(
        'invoice/partial-update/<str:invoice_id>/', 
        InvoiceAPIView.as_view(), 
        name='invoice-partial-update'
        ), #patch
    path(
        'invoice/delete/<str:invoice_id>/', 
        InvoiceAPIView.as_view(),
        name='invoice-delete'
        ), #delete

    path(
        'invoice/get/<str:invoice_id>/',
        SingleInvoiceAPIView.as_view(),
        name='invoice-get'
        ), #get single

    path(
        'invoice-detail/partial-update/<str:invoice_detail_id>/', 
        InvoiceDetailAPIView.as_view(), 
        name='invoice-detail-partial-update'
        ), #patch
    path(
        'invoice-detail/delete/<str:invoice_detail_id>/', 
        InvoiceDetailAPIView.as_view(), 
        name='invoice-detail-delete'
        ), #delete
]