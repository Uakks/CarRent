from typing import Any

from rest_framework import serializers

from apps.cars.models import Car
from apps.matching.models import CarSearchQuery


class CarMatchFilterSerializer(serializers.Serializer):
    """Serializer for validating car matching query parameters."""

    model = serializers.CharField(
        required=False,
        allow_blank=False,
    )
    year = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    min_price = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
    )
    max_price = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
    )
    is_available = serializers.BooleanField(
        required=False,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate that min_price does not exceed max_price."""
        min_price = attrs.get("min_price")
        max_price = attrs.get("max_price")

        if min_price is not None and max_price is not None and min_price > max_price:
            raise serializers.ValidationError(
                {"max_price": "Must be greater than or equal to min_price."}
            )

        return attrs


class MatchedCarSerializer(serializers.ModelSerializer):
    """Serializer representing car match search results."""

    class Meta:
        model = Car
        fields = (
            "car_id",
            "model",
            "year",
            "price_per_day",
            "description",
            "is_available",
        )


class CarSearchQuerySerializer(serializers.ModelSerializer):
    """Serializer for car search queries history."""

    class Meta:
        model = CarSearchQuery
        fields = (
            "search_id",
            "user",
            "model",
            "year",
            "min_price",
            "max_price",
            "results_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "search_id",
            "results_count",
            "created_at",
            "updated_at",
        )
