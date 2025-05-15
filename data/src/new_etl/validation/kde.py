from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class KDEValidator(ServiceValidator):
    """
    Validator for KDE (Kernel Density Estimation) data.
    Ensures proper data quality and consistency for KDE assignments.
    """

    VALID_DENSITY_LABELS = {"low", "medium", "high"}

    def __init__(self):
        super().__init__()
        self.density_column = None
        self.zscore_column = None
        self.label_column = None
        self.percentile_column = None

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the KDE data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = [
            self.density_column,
            self.zscore_column,
            self.label_column,
            self.percentile_column,
        ]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid density labels
        if self.label_column in data.columns:
            invalid_labels = data[
                ~data[self.label_column].isin(self.VALID_DENSITY_LABELS)
            ]
            if not invalid_labels.empty:
                errors.append(
                    f"Found {len(invalid_labels)} properties with invalid {self.label_column} values. Valid labels are: {', '.join(sorted(self.VALID_DENSITY_LABELS))}"
                )

        # Check percentile bounds (0 to 100)
        if self.percentile_column in data.columns:
            invalid_percentiles = data[
                (data[self.percentile_column] < 0)
                | (data[self.percentile_column] > 100)
            ]
            if not invalid_percentiles.empty:
                errors.append(
                    f"Found {len(invalid_percentiles)} properties with {self.percentile_column} values outside [0,100] range"
                )

        # Log statistics about KDE assignments
        if all(col in data.columns for col in required_columns):
            total_properties = len(data)
            print("\nKDE Statistics:")
            print(f"- Total properties: {total_properties}")

            # Density label distribution
            label_counts = data[self.label_column].value_counts()
            print("\nDensity Label Distribution:")
            for label, count in label_counts.items():
                percentage = (count / total_properties) * 100
                print(f"- {label}: {count} properties ({percentage:.1f}%)")

            # Percentile distribution
            percentile_ranges = [
                (0, 20, "0-20%"),
                (20, 40, "20-40%"),
                (40, 60, "40-60%"),
                (60, 80, "60-80%"),
                (80, 100, "80-100%"),
            ]

            print("\nPercentile Distribution:")
            for start, end, label in percentile_ranges:
                count = len(
                    data[
                        (data[self.percentile_column] >= start)
                        & (data[self.percentile_column] < end)
                    ]
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
        if not all(
            [
                self.density_column,
                self.zscore_column,
                self.label_column,
                self.percentile_column,
            ]
        ):
            return []
        return [
            self.density_column,
            self.zscore_column,
            self.label_column,
            self.percentile_column,
        ]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        if not self.label_column:
            return {}
        return {self.label_column: self.VALID_DENSITY_LABELS}

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
