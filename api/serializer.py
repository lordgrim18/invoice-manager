from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)

    class Meta:
        model = InvoiceDetail
        fields = [
            # 'id',
            'description', 
            'quantity', 
            'unit_price', 
            'price'
            ]
        
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.price = validated_data.get('price', instance.price)
        if instance.quantity or instance.unit_price:
            if not validated_data.get('price'):
                instance.price = float(instance.quantity) * float(instance.unit_price)
        instance.save()
        return instance
        
class InvoiceSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)
    invoice_details = InvoiceDetailSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = [
            # 'id',
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
    
    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.invoice_date = validated_data.get('invoice_date', instance.invoice_date)
        instance.save()
        
        invoice_details_data = validated_data.get('invoice_details', [])
        if invoice_details_data:
            InvoiceDetail.objects.filter(invoice=instance).delete()
        for detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['invoice_date'] = instance.invoice_date.strftime('%Y-%m-%d')
        return response