from typing import List, Tuple

import geopandas as gpd
import pandas as pd

from .base_validator import BaseValidator


class PPRPropertiesValidator(BaseValidator):
    """
    Validator for PPR (Philadelphia Parks & Recreation) properties.
    Ensures data quality and proper masking of park properties.
    """

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the PPR properties data and their impact on the primary feature layer.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate.

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check required columns
        required_columns = ["geometry", "vacant", "public_name"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check that 'vacant' column is boolean
        if "vacant" in gdf.columns and not pd.api.types.is_bool_dtype(gdf["vacant"]):
            errors.append("'vacant' column must be of boolean type")

        # Check for null geometries
        null_geoms = gdf["geometry"].isna().sum()
        if null_geoms > 0:
            errors.append(f"Found {null_geoms} null geometries")

        # Check for invalid geometries
        invalid_geoms = ~gdf["geometry"].is_valid
        if invalid_geoms.any():
            errors.append(f"Found {invalid_geoms.sum()} invalid geometries")

        # Check number of properties being masked
        if "public_name" in gdf.columns:
            mask = gdf["public_name"].notnull()
            count_masked = mask.sum()
            if count_masked < 400:
                errors.append(
                    f"Too few PPR properties being masked: {count_masked} (expected: 400-600)"
                )
            elif count_masked > 600:
                errors.append(
                    f"Too many PPR properties being masked: {count_masked} (expected: 400-600)"
                )

            # Log statistics about masking
            total_properties = len(gdf)
            percent_masked = (count_masked / total_properties) * 100
            print("PPR properties masking statistics:")
            print(f"- Total properties: {total_properties}")
            print(f"- Properties being masked: {count_masked}")
            print(f"- Percentage masked: {percent_masked:.2f}%")
            if count_masked < 400 or count_masked > 600:
                print(f"WARNING: Expected 400-600 PPR properties, found {count_masked}")

        return len(errors) == 0, errors
