from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    is_paid=serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'order',
            'start_datetime',
            'total_price',
            'paid_at',
            'is_paid',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['payment_id','paid_at','created_at', 'updated_at']
