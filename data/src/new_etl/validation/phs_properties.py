from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class PHSPropertiesValidator(ServiceValidator):
    """
    Validator for Philadelphia Housing Services (PHS) properties data.
    Ensures proper data quality and consistency for PHS property assignments.
    """

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the PHS properties data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "phs_property"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid PHS property values
        if "phs_property" in data.columns:
            invalid_values = data[~data["phs_property"].isin([True, False])]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with invalid phs_property values. Valid values are: True, False"
                )

        # Log statistics about PHS properties
        if "phs_property" in data.columns:
            total_properties = len(data)
            phs_properties = data[data["phs_property"]].shape[0]
            print("\nPHS Properties Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- PHS properties: {phs_properties} ({phs_properties / total_properties * 100:.1f}%)"
            )

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "phs_property"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {"phs_property": {True, False}}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the PHS properties data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "phs_property"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[gdf[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid PHS property values
        if "phs_property" in gdf.columns:
            invalid_values = gdf[~gdf["phs_property"].isin([True, False])]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with invalid phs_property values. Valid values are: True, False"
                )

        # Log statistics about PHS properties
        if "phs_property" in gdf.columns:
            total_properties = len(gdf)
            phs_properties = gdf[gdf["phs_property"]].shape[0]
            print("\nPHS Properties Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- PHS properties: {phs_properties} ({phs_properties / total_properties * 100:.1f}%)"
            )

        return len(errors) == 0, errors
