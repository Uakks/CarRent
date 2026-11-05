from typing import Any

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cars.models import Car
from apps.matching.models import CarSearchQuery
from apps.matching.serializers import (
    CarMatchFilterSerializer,
    CarSearchQuerySerializer,
    MatchedCarSerializer,
)


class CarMatchingListView(ListAPIView):
    """API endpoint to list and match cars based on search criteria."""

    serializer_class = MatchedCarSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        filters = CarMatchFilterSerializer(data=self.request.query_params.dict())
        filters.is_valid(raise_exception=True)
        values = filters.validated_data

        queryset = Car.objects.filter(deleted_at__isnull=True)
        if "is_available" in values:
            queryset = queryset.filter(is_available=values["is_available"])
        else:
            queryset = queryset.filter(is_available=True)

        if "model" in values:
            queryset = queryset.filter(model__icontains=values["model"])
        if "year" in values:
            queryset = queryset.filter(year=values["year"])
        if "min_price" in values:
            queryset = queryset.filter(price_per_day__gte=values["min_price"])
        if "max_price" in values:
            queryset = queryset.filter(price_per_day__lte=values["max_price"])

        return queryset.order_by("price_per_day", "year")

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle GET request and log search query history."""
        response: Response = super().list(request, *args, **kwargs)

        try:
            filters = CarMatchFilterSerializer(data=request.query_params.dict())
            if filters.is_valid():
                validated = filters.validated_data
                user = request.user if request.user and request.user.is_authenticated else None
                found_count = len(response.data) if isinstance(response.data, list) else 0

                CarSearchQuery.objects.create(
                    user=user,
                    model=validated.get("model", ""),
                    year=validated.get("year"),
                    min_price=validated.get("min_price"),
                    max_price=validated.get("max_price"),
                    results_count=found_count,
                )
        except Exception:
            pass

        return response


class CarSearchQueryViewSet(viewsets.ModelViewSet):
    """ViewSet for listing, creating, and inspecting car search query records."""

    queryset = CarSearchQuery.objects.filter(deleted_at__isnull=True)
    serializer_class = CarSearchQuerySerializer
    permission_classes = [AllowAny]
