from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(deleted_at__isnull=True)
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        payment = self.get_object()
        if payment.is_paid:
            return Response(
                {'detail': 'Payment has already been completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.mark_as_paid()
        return Response(
            {
                'detail': 'Payment completed successfully.',
                'payment': PaymentSerializer(payment).data
            },
            status=status.HTTP_200_OK
        )