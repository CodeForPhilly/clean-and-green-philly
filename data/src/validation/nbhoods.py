from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class NeighborhoodsValidator(ServiceValidator):
    """Validator for neighborhoods service."""

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate neighborhoods data.

        Critical checks:
        - Required fields present (nbhood, geometry)
        - Neighborhood names are strings
        - Valid geometries
        - No duplicate neighborhoods
        - All observations have a neighborhood
        - Expected number of unique neighborhoods (~160)

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(self.check_required_columns(data, ["nbhood", "geometry"]))

        # Check data types
        if "nbhood" in data.columns and data["nbhood"].dtype != "object":
            errors.append("nbhood must be string type")

        # Check for duplicate neighborhoods
        errors.extend(self.check_duplicates(data, "nbhood"))

        # Check null values in critical fields
        errors.extend(
            self.check_null_percentage(data, "nbhood", threshold=0.0)
        )  # No nulls allowed

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check that all observations have a neighborhood
        if "nbhood" in data.columns:
            null_nbhoods = data["nbhood"].isnull().sum()
            if null_nbhoods > 0:
                errors.append(
                    f"Found {null_nbhoods} observations without a neighborhood"
                )

        # Check number of unique neighborhoods
        if "nbhood" in data.columns:
            unique_nbhoods = data["nbhood"].nunique()
            if unique_nbhoods < 100 or unique_nbhoods > 200:
                errors.append(
                    f"Expected around 150 unique neighborhoods, found {unique_nbhoods}"
                )

        return len(errors) == 0, errors
