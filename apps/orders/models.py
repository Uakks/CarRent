import uuid 
from decimal import Decimal 
from typing import TYPE_CHECKING 
from django.db import models 
from core.models import AbstractBaseModel

if TYPE_CHECKING:
    from users.models import CustomUser 
    from cars.models import Car 

class Order(AbstractBaseModel):
    """Модель заказа автомобиля"""

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    car=models.ForeignKey(
        "cars.Car",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Автомобиль",
    )
    start_datetime=models.DateTimeField(verbose_name="Дата и время начала")
    end_datetime=models.DateTimeField(verbose_name="Дата и время окончания")
    total_price=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-start_datetime"]

    def __str__(self) -> str:
        return f"Заказ {self.order_id} ({self.user})"

