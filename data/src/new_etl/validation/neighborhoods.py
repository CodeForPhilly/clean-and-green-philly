from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class NeighborhoodsValidator(ServiceValidator):
    """
    Validator for neighborhoods data.
    Ensures proper data quality and consistency for neighborhood boundaries.
    """

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the neighborhoods data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["name", "geometry"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for empty geometries
        if "geometry" in data.columns:
            empty_geoms = data[data.geometry.is_empty]
            if not empty_geoms.empty:
                errors.append(f"Found {len(empty_geoms)} empty geometries")

        # Check for invalid geometries
        if "geometry" in data.columns:
            invalid_geoms = data[~data.geometry.is_valid]
            if not invalid_geoms.empty:
                errors.append(f"Found {len(invalid_geoms)} invalid geometries")

        # Check for duplicate neighborhood names
        if "name" in data.columns:
            duplicates = data[data.duplicated(subset=["name"], keep=False)]
            if not duplicates.empty:
                errors.append(
                    f"Found {len(duplicates)} duplicate neighborhood names: {', '.join(duplicates['name'].unique())}"
                )

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["name", "geometry"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the neighborhoods data.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check for required columns
        required_columns = ["name", "geometry"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[gdf[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for empty geometries
        if "geometry" in gdf.columns:
            empty_geoms = gdf[gdf.geometry.is_empty]
            if not empty_geoms.empty:
                errors.append(f"Found {len(empty_geoms)} empty geometries")

        # Check for invalid geometries
        if "geometry" in gdf.columns:
            invalid_geoms = gdf[~gdf.geometry.is_valid]
            if not invalid_geoms.empty:
                errors.append(f"Found {len(invalid_geoms)} invalid geometries")

        # Check for duplicate neighborhood names
        if "name" in gdf.columns:
            duplicates = gdf[gdf.duplicated(subset=["name"], keep=False)]
            if not duplicates.empty:
                errors.append(
                    f"Found {len(duplicates)} duplicate neighborhood names: {', '.join(duplicates['name'].unique())}"
                )

        # Log statistics about the neighborhoods
        if "name" in gdf.columns:
            total_neighborhoods = len(gdf)
            print("\nNeighborhoods Statistics:")
            print(f"- Total neighborhoods: {total_neighborhoods}")
            print(f"- Unique neighborhood names: {gdf['name'].nunique()}")

        return len(errors) == 0, errors
