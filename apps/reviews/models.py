import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.abstracts.models import AbstractBaseModel


class Review(AbstractBaseModel):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Review ID'
    )
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Order'
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='User'
    )
    review_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('1.0')),
            MaxValueValidator(Decimal('5.0')),
        ],
        verbose_name='Review Score'
    )
    comment = models.TextField(
        blank=True,
        default='',
        verbose_name='Comment'
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-created_at',)

    def __str__(self):
        return f"Review {self.review_id} | Score: {self.review_score}"