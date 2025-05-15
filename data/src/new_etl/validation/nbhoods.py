from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class NeighborhoodsValidator(ServiceValidator):
    """
    Validator for neighborhood assignments.
    Ensures proper data quality and consistency for neighborhood assignments to properties.
    """

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate neighborhood assignments.

        Critical checks:
        - Required fields present (neighborhood, geometry)
        - Neighborhood names are strings
        - Valid geometries
        - All observations have a neighborhood
        - Expected number of unique neighborhoods (~160)

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        required_columns = ["neighborhood", "geometry"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check data types
        if "neighborhood" in data.columns and data["neighborhood"].dtype != "object":
            errors.append("neighborhood must be string type")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[col].isna().sum()
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check number of unique neighborhoods
        if "neighborhood" in data.columns:
            unique_nbhoods = data["neighborhood"].nunique()
            if unique_nbhoods < 100 or unique_nbhoods > 200:
                errors.append(
                    f"Expected around 150 unique neighborhoods, found {unique_nbhoods}"
                )

        # Log statistics about the neighborhood assignments
        if "neighborhood" in data.columns:
            total_properties = len(data)
            print("\nNeighborhood Statistics:")
            print(f"- Total properties: {total_properties}")

            # Neighborhood distribution
            nbhood_counts = data["neighborhood"].value_counts()
            print("\nTop 10 neighborhoods by property count:")
            for nbhood, count in nbhood_counts.head(10).items():
                percentage = (count / total_properties) * 100
                print(f"- {nbhood}: {count} properties ({percentage:.1f}%)")

            print("\nBottom 10 neighborhoods by property count:")
            for nbhood, count in nbhood_counts.tail(10).items():
                percentage = (count / total_properties) * 100
                print(f"- {nbhood}: {count} properties ({percentage:.1f}%)")

        return len(errors) == 0, errors
