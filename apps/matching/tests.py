from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APITestCase

from apps.cars.models import Car
from apps.matching.forms import CarSearchQueryAdminForm
from apps.matching.models import CarSearchQuery


class CarMatchingTests(APITestCase):
    """Test suite for car matching endpoints, models, admin form, and management commands."""

    def setUp(self):
        self.owner = get_user_model().objects.create(
            email="owner@example.com",
            full_name="Car Owner",
        )
        self.car1 = Car.objects.create(
            owner=self.owner,
            model="Civic",
            year=2022,
            price_per_day="40.00",
        )
        self.car2 = Car.objects.create(
            owner=self.owner,
            model="Civic Type R",
            year=2024,
            price_per_day="80.00",
        )
        self.car3 = Car.objects.create(
            owner=self.owner,
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

    def test_search_query_is_logged_on_matching_request(self):
        initial_count = CarSearchQuery.objects.count()
        response = self.client.get(
            "/api/matching/cars/",
            {
                "model": "civic",
                "year": 2022,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CarSearchQuery.objects.count(), initial_count + 1)

        logged = CarSearchQuery.objects.latest("created_at")
        self.assertEqual(logged.model, "civic")
        self.assertEqual(logged.year, 2022)
        self.assertEqual(logged.results_count, 1)

    def test_car_search_query_model_methods(self):
        query = CarSearchQuery.objects.create(
            model="Civic",
            year=2022,
            min_price=Decimal("30.00"),
            max_price=Decimal("60.00"),
            results_count=2,
        )

        self.assertIn("Civic", str(query))
        self.assertIn("Found: 2", str(query))
        self.assertFalse(query.is_deleted)

        query.delete()
        query.refresh_from_db()
        self.assertTrue(query.is_deleted)
        self.assertIsNotNone(query.deleted_at)

    def test_car_search_query_viewset_list(self):
        CarSearchQuery.objects.create(
            model="Corolla",
            year=2021,
            results_count=3,
        )

        response = self.client.get("/api/matching/queries/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_admin_form_validation(self):
        form_valid = CarSearchQueryAdminForm(
            data={
                "model": " Camry ",
                "min_price": "20.00",
                "max_price": "50.00",
                "results_count": 5,
            }
        )
        self.assertTrue(form_valid.is_valid(), form_valid.errors)
        self.assertEqual(form_valid.cleaned_data["model"], "Camry")

        form_invalid = CarSearchQueryAdminForm(
            data={
                "model": "Camry",
                "min_price": "100.00",
                "max_price": "50.00",
                "results_count": 0,
            }
        )
        self.assertFalse(form_invalid.is_valid())
        self.assertIn("__all__", form_invalid.errors)

    def test_generatesearches_command(self):
        out = StringIO()
        call_command("generatesearches", 5, "--model", "Civic", stdout=out)
        self.assertIn("Successfully created 5 search queries", out.getvalue())
        self.assertEqual(CarSearchQuery.objects.filter(model="Civic").count(), 5)
