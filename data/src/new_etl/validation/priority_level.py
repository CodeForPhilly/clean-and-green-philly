from typing import Dict, List, Set

import geopandas as gpd

from .base import ServiceValidator


class PriorityLevelValidator(ServiceValidator):
    """
    Validator for priority level data.
    Ensures proper data quality and consistency for priority level assignments.
    """

    VALID_PRIORITY_LEVELS = {"low", "medium", "high", "unknown"}

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the priority level data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "priority_level"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid priority levels
        if "priority_level" in data.columns:
            invalid_levels = data[
                ~data["priority_level"].isin(self.VALID_PRIORITY_LEVELS)
            ]
            if not invalid_levels.empty:
                errors.append(
                    f"Found {len(invalid_levels)} properties with invalid priority_level values. Valid levels are: {', '.join(sorted(self.VALID_PRIORITY_LEVELS))}"
                )

        # Log statistics about priority levels
        if "priority_level" in data.columns:
            total_properties = len(data)
            print("\nPriority Level Statistics:")
            print(f"- Total properties: {total_properties}")

            # Priority level distribution
            priority_counts = data["priority_level"].value_counts()
            print("\nPriority Level Distribution:")
            for level, count in priority_counts.items():
                percentage = (count / total_properties) * 100
                print(f"- {level}: {count} properties ({percentage:.1f}%)")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "priority_level"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {"priority_level": self.VALID_PRIORITY_LEVELS}

    def validate(self, gdf: gpd.GeoDataFrame) -> tuple[bool, List[str]]:
        """
        Validate the priority level data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "priority_level"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[gdf[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid priority levels
        if "priority_level" in gdf.columns:
            invalid_levels = gdf[
                ~gdf["priority_level"].isin(self.VALID_PRIORITY_LEVELS)
            ]
            if not invalid_levels.empty:
                errors.append(
                    f"Found {len(invalid_levels)} properties with invalid priority_level values. Valid levels are: {', '.join(self.VALID_PRIORITY_LEVELS)}"
                )

        # Log statistics about the priority levels
        if "priority_level" in gdf.columns:
            total_properties = len(gdf)
            print("\nPriority Level Statistics:")
            print(f"- Total properties: {total_properties}")
            for level in self.VALID_PRIORITY_LEVELS:
                count = len(gdf[gdf["priority_level"] == level])
                print(f"- {level}: {count}")

        return len(errors) == 0, errors
