from django.conf import settings
from django.db import models
import uuid

from apps.abstracts.models import AbstractBaseModel


class Car(AbstractBaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
    )
    car_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.year} {self.model}"