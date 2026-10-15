import uuid
from django.db import models
from apps.abstracts.models import AbstractBaseModel


class Payment(AbstractBaseModel):
    payment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Payment ID'
    )
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True,
        verbose_name='Order'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Start Datetime'
    )
    total_price = models.DecimalField(
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
        ordering = ('-created_at',)

    def __str__(self):
        return f"Payment {self.payment_id}"