from rest_framework import serializers, validators
from .models import Invoice, InvoiceDetail
from datetime import datetime
from django.utils import timezone

class InvoiceDetailSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)
    price = serializers.FloatField(required=False)

    class Meta:
        model = InvoiceDetail
        fields = [
            # 'id',
            'description', 
            'quantity', 
            'unit_price', 
            'price'
            ]

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be less than 0")
        return value
    
    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be less than 0")
        return value
    
    def validate(self, data):
        if not data:
            raise serializers.ValidationError("request body cannot be empty")
        data['price'] = float(data.get('quantity')) * float(data.get('unit_price'))
        return data
        
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.price = instance.unit_price * instance.quantity
        instance.save()
        return instance
    
class InvoiceSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)
    invoice_details = InvoiceDetailSerializer(many=True)
    invoice_date = serializers.DateField(required=False)
    
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
        if not validated_data.get('invoice_date'):
            validated_data['invoice_date'] = timezone.now().strftime('%Y-%m-%d')
        invoice = Invoice.objects.create(**validated_data)
        for invoice_detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=invoice, **invoice_detail_data)
        return invoice
    
    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        invoice_date = validated_data.get('invoice_date', instance.invoice_date)
        instance.invoice_date = invoice_date.strftime('%Y-%m-%d')
        instance.save()
        
        invoice_details_data = validated_data.get('invoice_details', [])
        if invoice_details_data:
            InvoiceDetail.objects.filter(invoice=instance).delete()
            for detail_data in invoice_details_data:
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
    
    def validate(self, data):
        request = self.context.get('request')
        if not request.method == 'PATCH':
            if not data.get('invoice_details'):
                raise serializers.ValidationError("invoice details cannot be empty")
        else:
            if not data:
                raise serializers.ValidationError("request body cannot be empty")
            if 'invoice_details' in data:
                raise serializers.ValidationError("invoice details cannot be updated using this endpoint")
            
        customer_name = data.get('customer_name')
        invoice_date = data.get('invoice_date', timezone.now().strftime('%Y-%m-%d'))
        if Invoice.objects.filter(customer_name=customer_name, invoice_date=invoice_date).exists():
            raise serializers.ValidationError({
                "duplicate_value_error": "invoice already exists for the customer on the same date",
                "additional_message": "use the invoice-detail-create endpoint to add more details to the existing invoice",
                "invoice_id": Invoice.objects.get(customer_name=customer_name, invoice_date=invoice_date).id
            })
        
        return data
    
class MinimalInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer_name', 
            'invoice_date'
            ]