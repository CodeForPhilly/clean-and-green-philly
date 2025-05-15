from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class TreeCanopyValidator(ServiceValidator):
    """
    Validator for tree canopy data.
    Ensures proper data quality and consistency for tree canopy coverage assignments.
    """

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the tree canopy data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "tree_canopy"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid tree canopy values (0 to 1)
        if "tree_canopy" in data.columns:
            invalid_values = data[(data["tree_canopy"] < 0) | (data["tree_canopy"] > 1)]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with tree_canopy values outside [0,1] range"
                )

        # Log statistics about tree canopy coverage
        if "tree_canopy" in data.columns:
            total_properties = len(data)
            print("\nTree Canopy Statistics:")
            print(f"- Total properties: {total_properties}")
            print(f"- Mean tree canopy coverage: {data['tree_canopy'].mean():.1%}")
            print(f"- Median tree canopy coverage: {data['tree_canopy'].median():.1%}")
            print(f"- Min tree canopy coverage: {data['tree_canopy'].min():.1%}")
            print(f"- Max tree canopy coverage: {data['tree_canopy'].max():.1%}")

            # Distribution of tree canopy coverage
            coverage_ranges = [
                (0, 0.1, "0-10%"),
                (0.1, 0.2, "10-20%"),
                (0.2, 0.3, "20-30%"),
                (0.3, 0.4, "40-50%"),
                (0.4, 0.5, "50-60%"),
                (0.5, 0.6, "60-70%"),
                (0.6, 0.7, "70-80%"),
                (0.7, 0.8, "80-90%"),
                (0.8, 0.9, "90-100%"),
            ]

            print("\nTree Canopy Coverage Distribution:")
            for start, end, label in coverage_ranges:
                count = len(
                    data[(data["tree_canopy"] >= start) & (data["tree_canopy"] < end)]
                )
                percentage = (count / total_properties) * 100
                print(f"- {label}: {count} properties ({percentage:.1f}%)")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "tree_canopy"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the tree canopy data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "tree_canopy"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[gdf[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid tree canopy values (0 to 1)
        if "tree_canopy" in gdf.columns:
            invalid_values = gdf[(gdf["tree_canopy"] < 0) | (gdf["tree_canopy"] > 1)]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with tree_canopy values outside [0,1] range"
                )

        # Log statistics about tree canopy coverage
        if "tree_canopy" in gdf.columns:
            total_properties = len(gdf)
            print("\nTree Canopy Statistics:")
            print(f"- Total properties: {total_properties}")
            print(f"- Mean tree canopy coverage: {gdf['tree_canopy'].mean():.1%}")
            print(f"- Median tree canopy coverage: {gdf['tree_canopy'].median():.1%}")
            print(f"- Min tree canopy coverage: {gdf['tree_canopy'].min():.1%}")
            print(f"- Max tree canopy coverage: {gdf['tree_canopy'].max():.1%}")

            # Distribution of tree canopy coverage
            coverage_ranges = [
                (0, 0.1, "0-10%"),
                (0.1, 0.2, "10-20%"),
                (0.2, 0.3, "20-30%"),
                (0.3, 0.4, "40-50%"),
                (0.4, 0.5, "50-60%"),
                (0.5, 0.6, "60-70%"),
                (0.6, 0.7, "70-80%"),
                (0.7, 0.8, "80-90%"),
                (0.8, 0.9, "90-100%"),
            ]

            print("\nTree Canopy Coverage Distribution:")
            for start, end, label in coverage_ranges:
                count = len(
                    gdf[(gdf["tree_canopy"] >= start) & (gdf["tree_canopy"] < end)]
                )
                percentage = (count / total_properties) * 100
                print(f"- {label}: {count} properties ({percentage:.1f}%)")

        return len(errors) == 0, errors
