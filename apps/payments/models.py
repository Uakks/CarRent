import uuid
from django.db import models
from django.utils import timezone
from apps.abstracts.models import AbstractBaseModel


class Payment(AbstractBaseModel):

    payment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Payment_ID'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True,
        verbose_name='Order'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Start Datetime'
    )

    total_price =models.DecimalField (
        max_digits=10,
        decimal_places=2,
        verbose_name='Total Price'
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Paid At'
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
    @property
    def is_paid(self) -> bool:
        return self.paid_at is not None
    
    def mark_as_paid(self) -> None:

        self.paid_at = timezone.now()
        self.save(update_fields=['paid_at','updated_at'])

    def __str__(self):
        status = "Paid" if self.is_paid else "Unpaid"
        return f"Payment {self.payment_id} | {self.total_price} | {status}"


