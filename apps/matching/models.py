import uuid

from django.conf import settings
from django.db.models import (
    CharField,
    CheckConstraint,
    DecimalField,
    ForeignKey,
    Index,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    Q,
    SET_NULL,
    UUIDField,
)

from apps.abstracts.models import AbstractBaseModel


class CarSearchQuery(AbstractBaseModel):
    """Car search query database model to track user car search history."""

    MODEL_MAX_LEN = 100
    PRICE_MAX_DIGITS = 10
    PRICE_DECIMAL_PLACES = 2

    search_id = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Search ID",
    )
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="search_queries",
        verbose_name="User",
    )
    model = CharField(
        max_length=MODEL_MAX_LEN,
        blank=True,
        default="",
        verbose_name="Searched Model",
    )
    year = PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Searched Year",
    )
    min_price = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name="Min Price",
    )
    max_price = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name="Max Price",
    )
    results_count = PositiveIntegerField(
        default=0,
        verbose_name="Results Found",
    )

    class Meta:
        verbose_name = "Car Search Query"
        verbose_name_plural = "Car Search Queries"
        ordering = ("-created_at",)
        constraints = [
            CheckConstraint(
                condition=Q(min_price__gte=0) | Q(min_price__isnull=True),
                name="check_matching_min_price_non_negative",
            ),
            CheckConstraint(
                condition=Q(max_price__gte=0) | Q(max_price__isnull=True),
                name="check_matching_max_price_non_negative",
            ),
            CheckConstraint(
                condition=Q(results_count__gte=0),
                name="check_matching_results_count_non_negative",
            ),
        ]
        indexes = [
            Index(fields=("user", "created_at"), name="matching_user_created_idx"),
            Index(fields=("model", "year"), name="matching_model_year_idx"),
        ]

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def __str__(self) -> str:
        model_name: str = self.model if self.model else "Any"
        return f"Search {self.search_id} | Model: {model_name} | Found: {self.results_count}"
