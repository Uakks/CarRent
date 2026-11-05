from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.matching.views import CarMatchingListView, CarSearchQueryViewSet

router = DefaultRouter()
router.register(r"queries", CarSearchQueryViewSet, basename="car-search-query")

urlpatterns = [
    path("cars/", CarMatchingListView.as_view(), name="matched-cars"),
    path("", include(router.urls)),
]
