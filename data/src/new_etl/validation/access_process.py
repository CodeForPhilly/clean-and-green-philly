from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class AccessProcessValidator(ServiceValidator):
    """
    Validator for access process data.
    Ensures proper data quality and consistency for access process assignments.
    """

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the access process data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "access_process"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid access process values
        if "access_process" in data.columns:
            valid_values = {"Yes", "No", "Unknown"}
            invalid_values = data[~data["access_process"].isin(valid_values)]
            if not invalid_values.empty:
                errors.append(
                    f"Found {len(invalid_values)} properties with invalid access_process values. Valid values are: {', '.join(sorted(valid_values))}"
                )

        # Log statistics about access process
        if "access_process" in data.columns:
            total_properties = len(data)
            print("\nAccess Process Statistics:")
            print(f"- Total properties: {total_properties}")

            # Access process distribution
            access_counts = data["access_process"].value_counts()
            print("\nAccess Process Distribution:")
            for status, count in access_counts.items():
                percentage = (count / total_properties) * 100
                print(f"- {status}: {count} properties ({percentage:.1f}%)")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "access_process"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {"access_process": {"Yes", "No", "Unknown"}}

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate access process data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        required_columns = self.get_required_input_columns()
        errors.extend(self.check_required_columns(data, required_columns))

        # Check required values
        required_values = self.get_required_input_values()
        for col, valid_set in required_values.items():
            if col in data.columns:
                invalid = data[~data[col].isin(valid_set)]
                if not invalid.empty:
                    errors.append(
                        f"Found {len(invalid)} rows with invalid values in {col}. Valid values: {', '.join(sorted(valid_set))}"
                    )

        # Service-specific validation
        errors.extend(self._validate_service_specific(data))

        return len(errors) == 0, errors
