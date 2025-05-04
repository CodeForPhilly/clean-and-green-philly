from typing import List, Tuple

import geopandas as gpd
import pandas as pd

from .base import ServiceValidator


class CouncilDistrictsValidator(ServiceValidator):
    """Validator for council districts service."""

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate council districts data.

        Critical checks:
        - Required fields present (district, geometry)
        - District numbers are valid (1-10) as strings
        - Valid geometries
        - No duplicate districts

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(self.check_required_columns(data, ["district", "geometry"]))

        # Check data types
        if "district" in data.columns and data["district"].dtype != "object":
            errors.append("district must be string type")

        # Check district number ranges
        if "district" in data.columns:
            try:
                # Convert to numeric for range checking
                districts = pd.to_numeric(data["district"])
                valid_districts = set(
                    range(1, 11)
                )  # Philadelphia has 10 council districts
                invalid_districts = set(districts.unique()) - valid_districts
                if invalid_districts:
                    errors.append(
                        f"Found invalid district numbers: {sorted(invalid_districts)}"
                    )
            except ValueError:
                errors.append(
                    "district values must be numeric strings between 1 and 10"
                )

        # Check for duplicate districts
        errors.extend(self.check_duplicates(data, "district"))

        # Check null values in critical fields
        errors.extend(
            self.check_null_percentage(data, "district", threshold=0.0)
        )  # No nulls allowed

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check record count (should be exactly 10 districts)
        if len(data) != 10:
            errors.append(f"Expected exactly 10 council districts, found {len(data)}")

        return len(errors) == 0, errors
