from typing import List, Tuple

import geopandas as gpd

from .base_validator import BaseValidator


class KDEValidator(BaseValidator):
    """
    Validator for Kernel Density Estimation (KDE) calculations.
    Ensures proper density calculations and data quality across all services that use KDE.
    """

    # Valid density labels
    VALID_DENSITY_LABELS = {"Low", "Medium", "High"}

    def __init__(self):
        """Initialize the validator with default column names."""
        self.density_column = None
        self.zscore_column = None
        self.label_column = None
        self.percentile_column = None

    def configure(
        self,
        density_column: str,
        zscore_column: str,
        label_column: str,
        percentile_column: str,
    ) -> "KDEValidator":
        """
        Configure the validator with the column names for a specific service.

        Args:
            density_column (str): Name of the density column
            zscore_column (str): Name of the z-score column
            label_column (str): Name of the density label column
            percentile_column (str): Name of the percentile column

        Returns:
            KDEValidator: The configured validator instance
        """
        self.density_column = density_column
        self.zscore_column = zscore_column
        self.label_column = label_column
        self.percentile_column = percentile_column
        return self

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the KDE calculations for a specific service.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        if not all(
            [
                self.density_column,
                self.zscore_column,
                self.label_column,
                self.percentile_column,
            ]
        ):
            return False, [
                "Validator not configured. Call configure() before validate()."
            ]

        errors = []

        # Check required columns
        required_columns = [
            self.density_column,
            self.zscore_column,
            self.label_column,
            self.percentile_column,
        ]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check density bounds (0 to 1)
        if self.density_column in gdf.columns:
            # Check for null values
            null_density = gdf[gdf[self.density_column].isna()]
            if not null_density.empty:
                errors.append(
                    f"Found {len(null_density)} properties with null {self.density_column}"
                )

            # Check bounds
            out_of_bounds = gdf[
                (gdf[self.density_column] < 0) | (gdf[self.density_column] > 1)
            ]
            if not out_of_bounds.empty:
                errors.append(
                    f"Found {len(out_of_bounds)} properties with density values outside [0,1] range"
                )

        # Check z-score bounds (-10 to 10)
        if self.zscore_column in gdf.columns:
            # Check for null values
            null_zscore = gdf[gdf[self.zscore_column].isna()]
            if not null_zscore.empty:
                errors.append(
                    f"Found {len(null_zscore)} properties with null {self.zscore_column}"
                )

            # Check bounds
            out_of_bounds = gdf[
                (gdf[self.zscore_column] < -10) | (gdf[self.zscore_column] > 10)
            ]
            if not out_of_bounds.empty:
                errors.append(
                    f"Found {len(out_of_bounds)} properties with z-score values outside [-10,10] range"
                )

        # Check density label
        if self.label_column in gdf.columns:
            # Check for null values
            null_labels = gdf[gdf[self.label_column].isna()]
            if not null_labels.empty:
                errors.append(
                    f"Found {len(null_labels)} properties with null {self.label_column}"
                )

            # Check valid values
            invalid_labels = gdf[
                ~gdf[self.label_column].isin(self.VALID_DENSITY_LABELS)
            ]
            if not invalid_labels.empty:
                errors.append(
                    f"Found {len(invalid_labels)} properties with invalid density labels. Valid labels are: {', '.join(self.VALID_DENSITY_LABELS)}"
                )

        # Check percentile bounds (0 to 100)
        if self.percentile_column in gdf.columns:
            # Check for null values
            null_percentile = gdf[gdf[self.percentile_column].isna()]
            if not null_percentile.empty:
                errors.append(
                    f"Found {len(null_percentile)} properties with null {self.percentile_column}"
                )

            # Check bounds
            out_of_bounds = gdf[
                (gdf[self.percentile_column] < 0) | (gdf[self.percentile_column] > 100)
            ]
            if not out_of_bounds.empty:
                errors.append(
                    f"Found {len(out_of_bounds)} properties with percentile values outside [0,100] range"
                )

        # Log statistics about the density calculations
        if all(col in gdf.columns for col in [self.density_column, self.label_column]):
            total_properties = len(gdf)
            print(f"\n{self.density_column} Statistics:")
            print(f"- Total properties: {total_properties}")

            # Density label distribution
            for label in self.VALID_DENSITY_LABELS:
                count = len(gdf[gdf[self.label_column] == label])
                percentage = (count / total_properties) * 100
                print(f"- {label} density: {count} ({percentage:.1f}%)")

            # Density value statistics
            if self.density_column in gdf.columns:
                print("\nDensity Value Statistics:")
                print(f"- Mean: {gdf[self.density_column].mean():.3f}")
                print(f"- Median: {gdf[self.density_column].median():.3f}")
                print(f"- Min: {gdf[self.density_column].min():.3f}")
                print(f"- Max: {gdf[self.density_column].max():.3f}")

        return len(errors) == 0, errors
