from typing import Any

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput

from apps.matching.models import CarSearchQuery


class CarSearchQueryAdminForm(ModelForm):
    """CarSearchQuery form for the admin panel."""

    class Meta:
        model = CarSearchQuery
        fields = "__all__"
        widgets = {
            "model": TextInput(attrs={"placeholder": "e.g. Civic, Camry"}),
        }

    def clean_model(self) -> str:
        """Clean and strip model input string."""
        model: str = self.cleaned_data.get("model", "")
        return model.strip()

    def clean(self) -> dict[str, Any]:
        """Validate multi-field consistency between min_price and max_price."""
        cleaned_data: dict[str, Any] = super().clean()
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")

        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValidationError("Minimum price cannot exceed maximum price.")

        return cleaned_data
