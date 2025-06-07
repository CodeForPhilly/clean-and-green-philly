from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class AccessProcessValidator(ServiceValidator):
    """Validator for access process service."""

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate access process data.

        Critical checks:
        - Required fields present (opa_id, access_process)
        - No duplicate opa_ids
        - Valid geometries
        - Valid access process values

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(self.check_required_columns(data, ["opa_id", "access_process"]))

        # Check for duplicate opa_ids
        errors.extend(self.check_duplicates(data, "opa_id"))

        # Check data types
        if "opa_id" in data.columns and not data["opa_id"].dtype == "object":
            errors.append("opa_id must be string type")
        if (
            "access_process" in data.columns
            and not data["access_process"].dtype == "object"
        ):
            errors.append("access_process must be string type")

        # Check null values in critical fields
        errors.extend(
            self.check_null_percentage(data, "opa_id", threshold=0.0)
        )  # No nulls allowed
        errors.extend(
            self.check_null_percentage(data, "access_process", threshold=0.0)
        )  # No nulls allowed

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        total_count = len(data)

        # Check for valid access process values
        valid_processes = {
            "Go through Land Bank",
            "Do Nothing",
            "Private Land Use Agreement",
            "Buy Property",
        }
        invalid_processes = set(data["access_process"].unique()) - valid_processes
        if invalid_processes:
            errors.append(
                f"Found invalid access processes: {', '.join(invalid_processes)}"
            )

        # Log statistics about access processes
        print("\nAccess Process Statistics:")
        print(f"- Total properties: {total_count}")

        for process in sorted(valid_processes):
            count = len(data[data["access_process"] == process])
            print(f"- {process}: {count} ({count / total_count:.1%})")

        return len(errors) == 0, errors
