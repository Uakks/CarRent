import time
from decimal import Decimal
from random import choice, randint
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.matching.models import CarSearchQuery


class Command(BaseCommand):
    """Management command to generate sample car search queries in bulk."""

    help = "Generate fake car search queries."

    SAMPLE_MODELS = (
        "Camry",
        "Corolla",
        "Civic",
        "Accord",
        "Model 3",
        "Model Y",
        "Tiguan",
        "Golf",
        "RAV4",
        "BMW 3 Series",
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Define command-line arguments."""
        parser.add_argument(
            "count",
            type=int,
            help="How many search queries to create",
        )
        parser.add_argument(
            "--model",
            type=str,
            default="",
            help="Specific model name to assign to generated queries",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Command entry point."""
        count: int = options["count"]
        custom_model: str = options["model"]

        if count <= 0:
            raise CommandError("count must be greater than 0")

        start_time: float = time.perf_counter()

        queries_to_create: list[CarSearchQuery] = []
        for _ in range(count):
            model_name = custom_model if custom_model else choice(self.SAMPLE_MODELS)
            min_p = Decimal(randint(20, 50))
            max_p = min_p + Decimal(randint(10, 100))
            year = choice([None, 2020, 2021, 2022, 2023, 2024])

            queries_to_create.append(
                CarSearchQuery(
                    model=model_name,
                    year=year,
                    min_price=min_p,
                    max_price=max_p,
                    results_count=randint(0, 15),
                )
            )

        CarSearchQuery.objects.bulk_create(queries_to_create, batch_size=500)

        elapsed_seconds: float = time.perf_counter() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(queries_to_create)} search queries in {elapsed_seconds:.4f} seconds."
            )
        )
