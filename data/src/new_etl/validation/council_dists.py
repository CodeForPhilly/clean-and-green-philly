from typing import Dict, List, Set, Tuple

import geopandas as gpd
import pandas as pd

from .base import ServiceValidator


class CouncilDistrictsValidator(ServiceValidator):
    """
    Validator for council district assignments.
    Ensures proper data quality and consistency for council district assignments to properties.
    """

    VALID_DISTRICTS = {
        str(i) for i in range(1, 11)
    }  # Philadelphia has 10 council districts

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the council district assignments.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

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

        # Check for null values in critical fields
        if "district" in data.columns:
            null_districts = data["district"].isnull().sum()
            if null_districts > 0:
                errors.append(f"Found {null_districts} observations without a district")

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check that all valid districts are represented
        if "district" in data.columns:
            unique_districts = set(data["district"].dropna().unique())
            missing_districts = self.VALID_DISTRICTS - unique_districts
            if missing_districts:
                errors.append(
                    f"Missing assignments for districts: {', '.join(sorted(missing_districts))}"
                )

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["district", "geometry"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {"district": self.VALID_DISTRICTS}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the council district assignments.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check required columns
        required_columns = ["district", "geometry"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in gdf.columns:
                null_count = gdf[col].isna().sum()
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for invalid district values
        if "district" in gdf.columns:
            invalid_values = gdf[~gdf["district"].isin(self.VALID_DISTRICTS)]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with invalid district values"
                )

        # Log statistics about the district assignments
        if "district" in gdf.columns:
            total_properties = len(gdf)
            print("\nCouncil District Statistics:")
            print(f"- Total properties: {total_properties}")

            # District distribution
            district_counts = gdf["district"].value_counts()
            for district in sorted(self.VALID_DISTRICTS):
                count = district_counts.get(district, 0)
                percentage = (count / total_properties) * 100
                print(f"- District {district}: {count} properties ({percentage:.1f}%)")

        return len(errors) == 0, errors
