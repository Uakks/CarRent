from rest_framework.generics import ListAPIView

from apps.cars.models import Car
from .serializers import CarMatchFilterSerializer, MatchedCarSerializer


class CarMatchingListView(ListAPIView):
    serializer_class = MatchedCarSerializer

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
