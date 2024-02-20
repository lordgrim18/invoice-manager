from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceDetail
        fields = [
            'description', 
            'quantity', 
            'unit_price', 
            'price'
            ]
        
class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = [
            'customer_name', 
            'invoice_date', 
            'invoice_details'
            ]
        
    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details')
        invoice = Invoice.objects.create(**validated_data)
        for invoice_detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=invoice, **invoice_detail_data)
        return invoice
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['invoice_date'] = instance.invoice_date.strftime('%Y-%m-%d')
        return response
    
    def validate(self, data):
        if not data.get('invoice_details'):
            raise serializers.ValidationError("invoice_details is required")
        return data