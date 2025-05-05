from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class VacantPropertiesValidator(ServiceValidator):
    """Validator for vacant properties service."""

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate vacant properties data.

        Critical checks:
        - Required fields present (opa_id, parcel_type)
        - No duplicate opa_ids
        - Valid geometries
        - Expected number of records

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(self.check_required_columns(data, ["opa_id", "parcel_type"]))

        # Check for duplicate opa_ids
        errors.extend(self.check_duplicates(data, "opa_id"))

        # Check data types
        if "opa_id" in data.columns and not data["opa_id"].dtype == "object":
            errors.append("opa_id must be string type")
        if "parcel_type" in data.columns and not data["parcel_type"].dtype == "object":
            errors.append("parcel_type must be string type")

        # Check null values in critical fields
        errors.extend(
            self.check_null_percentage(data, "opa_id", threshold=0.0)
        )  # No nulls allowed
        errors.extend(
            self.check_null_percentage(data, "parcel_type", threshold=0.0)
        )  # No nulls allowed

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check record counts
        total_count = len(data)
        if total_count < 10000:
            errors.append(
                f"Total vacant properties count ({total_count}) is below minimum threshold (10000)"
            )

        # Check counts by parcel type
        if "parcel_type" in data.columns:
            building_count = len(data[data["parcel_type"] == "Building"])
            lot_count = len(data[data["parcel_type"] == "Land"])

            if building_count < 10000:
                errors.append(
                    f"Vacant building count ({building_count}) is below minimum threshold (10000)"
                )
            if lot_count < 20000:
                errors.append(
                    f"Vacant lot count ({lot_count}) is below minimum threshold (20000)"
                )

        return len(errors) == 0, errors
