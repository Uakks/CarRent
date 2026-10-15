import uuid
from django.db import models
from apps.abstracts.models import AbstractBaseModel


class Order(AbstractBaseModel):
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Order ID'
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.order_id}"
