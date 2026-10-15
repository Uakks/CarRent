from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.payments.models import Payment


class PaymentModelTest(TestCase):
    def test_payment_creation_and_pay_flow(self):
        now = timezone.now()
        payment = Payment.objects.create(
            start_datetime=now,
            total_price=Decimal('25000.00'),
        )
        self.assertIsNotNone(payment.payment_id)
        self.assertFalse(payment.is_paid)
        self.assertIsNone(payment.paid_at)

        payment.mark_as_paid()
        self.assertTrue(payment.is_paid)
        self.assertIsNotNone(payment.paid_at)

    def test_soft_delete(self):
        payment = Payment.objects.create(
            start_datetime=timezone.now(),
            total_price=Decimal('10000.00'),
        )
        payment.delete()
        payment.refresh_from_db()

        self.assertIsNotNone(payment.deleted_at)