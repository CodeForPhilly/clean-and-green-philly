from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class LIViolationsValidator(ServiceValidator):
    """
    Validator for L&I violations data.
    Ensures proper data quality and consistency for L&I violations assignments.
    """

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the L&I violations data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "li_violations"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid violation counts
        if "li_violations" in data.columns:
            invalid_values = data[data["li_violations"] < 0]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with negative violation counts"
                )

        # Log statistics about L&I violations
        if "li_violations" in data.columns:
            total_properties = len(data)
            print("\nL&I Violations Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- Properties with violations: {len(data[data['li_violations'] > 0])}"
            )
            print(f"- Total violations: {data['li_violations'].sum()}")
            print(f"- Mean violations per property: {data['li_violations'].mean():.2f}")
            print(
                f"- Median violations per property: {data['li_violations'].median():.2f}"
            )
            print(f"- Max violations on a property: {data['li_violations'].max()}")

            # Distribution of violation counts
            violation_ranges = [
                (0, 1, "0"),
                (1, 2, "1"),
                (2, 3, "2"),
                (3, 4, "3"),
                (4, 5, "4"),
                (5, 10, "5-9"),
                (10, 20, "10-19"),
                (20, 50, "20-49"),
                (50, float("inf"), "50+"),
            ]

            print("\nViolation Count Distribution:")
            for start, end, label in violation_ranges:
                count = len(
                    data[
                        (data["li_violations"] >= start) & (data["li_violations"] < end)
                    ]
                )
                percentage = (count / total_properties) * 100
                print(f"- {label} violations: {count} properties ({percentage:.1f}%)")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "li_violations"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the L&I violations data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "li_violations"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[gdf[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid violation counts
        if "li_violations" in gdf.columns:
            invalid_values = gdf[gdf["li_violations"] < 0]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with negative violation counts"
                )

        # Log statistics about L&I violations
        if "li_violations" in gdf.columns:
            total_properties = len(gdf)
            print("\nL&I Violations Statistics:")
            print(f"- Total properties: {total_properties}")
            print(f"- Properties with violations: {len(gdf[gdf['li_violations'] > 0])}")
            print(f"- Total violations: {gdf['li_violations'].sum()}")
            print(f"- Mean violations per property: {gdf['li_violations'].mean():.2f}")
            print(
                f"- Median violations per property: {gdf['li_violations'].median():.2f}"
            )
            print(f"- Max violations on a property: {gdf['li_violations'].max()}")

            # Distribution of violation counts
            violation_ranges = [
                (0, 1, "0"),
                (1, 2, "1"),
                (2, 3, "2"),
                (3, 4, "3"),
                (4, 5, "4"),
                (5, 10, "5-9"),
                (10, 20, "10-19"),
                (20, 50, "20-49"),
                (50, float("inf"), "50+"),
            ]

            print("\nViolation Count Distribution:")
            for start, end, label in violation_ranges:
                count = len(
                    gdf[(gdf["li_violations"] >= start) & (gdf["li_violations"] < end)]
                )
                percentage = (count / total_properties) * 100
                print(f"- {label} violations: {count} properties ({percentage:.1f}%)")

        return len(errors) == 0, errors
