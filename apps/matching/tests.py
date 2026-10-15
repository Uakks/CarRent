from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.cars.models import Car


class CarMatchingTests(APITestCase):
    def setUp(self):
        owner = get_user_model().objects.create(
            email="owner@example.com",
            full_name="Car Owner",
        )
        Car.objects.create(
            owner=owner,
            model="Civic",
            year=2022,
            price_per_day="40.00",
        )
        Car.objects.create(
            owner=owner,
            model="Civic Type R",
            year=2024,
            price_per_day="80.00",
        )
        Car.objects.create(
            owner=owner,
            model="Accord",
            year=2022,
            price_per_day="60.00",
            is_available=False,
        )

    def test_filters_available_cars_by_model_year_and_price(self):
        response = self.client.get(
            "/api/matching/cars/",
            {
                "model": "civic",
                "year": 2022,
                "min_price": "30.00",
                "max_price": "50.00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, response.data)
        self.assertEqual(response.data[0]["model"], "Civic")

    def test_can_include_unavailable_cars_explicitly(self):
        response = self.client.get(
            "/api/matching/cars/",
            {"is_available": "false"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["model"], "Accord")

    def test_rejects_inverted_price_range(self):
        response = self.client.get(
            "/api/matching/cars/",
            {"min_price": "80.00", "max_price": "40.00"},
        )

        self.assertEqual(response.status_code, 400)
