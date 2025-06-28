"""
Base test mixin for validator tests to eliminate repetitive test patterns.

This mixin provides common test methods that can be used across all validator tests,
reducing code duplication and ensuring consistent test coverage.
"""

from typing import Any, Callable, Dict, List, Type

import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.base import BaseValidator


class BaseValidatorTestMixin:
    """Mixin providing common validator test patterns."""

    def test_schema_valid_data(
        self,
        validator_class: Type[BaseValidator],
        valid_data_func: Callable,
        base_test_data: pd.DataFrame,
        check_stats: bool = False,
    ):
        """Test that the validator accepts valid data."""
        test_data = valid_data_func(base_test_data)
        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

        validator = validator_class()
        result = validator.validate(gdf, check_stats=check_stats)

        # Should pass with valid data
        assert result.success, f"Validation failed with errors: {result.errors}"
        assert len(result.errors) == 0

    def test_missing_required_columns(
        self,
        validator_class: Type[BaseValidator],
        required_columns: List[str],
        base_test_data: pd.DataFrame,
    ):
        """Test that the validator catches missing required columns."""
        for missing_col in required_columns:
            # Create test data missing the specific column
            test_data = {}
            for col in required_columns:
                if col != missing_col:
                    if col == "opa_id":
                        test_data[col] = base_test_data["opa_id"]
                    elif col == "geometry":
                        test_data[col] = base_test_data["geometry"]
                    else:
                        # For other columns, create appropriate dummy data based on expected type
                        test_data[col] = self._create_dummy_data_for_column(
                            col, len(base_test_data)
                        )

            # Always include geometry column from base_test_data
            test_data["geometry"] = base_test_data["geometry"]

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

            validator = validator_class()
            result = validator.validate(gdf, check_stats=False)

            # Should fail due to missing column
            assert (
                not result.success
            ), f"Validation should fail when missing {missing_col}"
            assert len(result.errors) > 0

    def test_null_values_in_required_columns(
        self,
        validator_class: Type[BaseValidator],
        required_columns: List[str],
        base_test_data: pd.DataFrame,
    ):
        """Test that the validator catches null values in required columns."""
        for col in required_columns:
            if col in ["opa_id", "geometry"]:
                continue  # Skip these as they're handled by base validator

            # Create test data with null in the specific column
            test_data = {}
            for req_col in required_columns:
                if req_col == "opa_id":
                    test_data[req_col] = base_test_data["opa_id"]
                elif req_col == "geometry":
                    test_data[req_col] = base_test_data["geometry"]
                elif req_col == col:
                    # Add null value to this column
                    dummy_data = self._create_dummy_data_for_column(
                        req_col, len(base_test_data)
                    )
                    dummy_data[1] = None  # Middle value is null
                    test_data[req_col] = dummy_data
                else:
                    # For other columns, create appropriate dummy data
                    test_data[req_col] = self._create_dummy_data_for_column(
                        req_col, len(base_test_data)
                    )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

            validator = validator_class()
            result = validator.validate(gdf, check_stats=False)

            # Should fail due to null values
            assert (
                not result.success
            ), f"Validation should fail when {col} has null values"
            assert len(result.errors) > 0

    def test_wrong_data_types(
        self,
        validator_class: Type[BaseValidator],
        column_specs: Dict[str, Dict[str, Any]],
        base_test_data: pd.DataFrame,
    ):
        """Test that the validator catches wrong data types."""
        for col, spec in column_specs.items():
            if col in ["opa_id", "geometry"]:
                continue  # Skip these as they're handled by base validator

            expected_type = spec.get("type")
            wrong_value = spec.get("wrong_value")

            if expected_type is None or wrong_value is None:
                continue

            # Create test data with wrong type for the specific column
            test_data = {}
            for req_col in column_specs.keys():
                if req_col == "opa_id":
                    test_data[req_col] = base_test_data["opa_id"]
                elif req_col == "geometry":
                    test_data[req_col] = base_test_data["geometry"]
                elif req_col == col:
                    # Add wrong type value to this column
                    dummy_data = self._create_dummy_data_for_column(
                        req_col, len(base_test_data)
                    )
                    dummy_data[1] = wrong_value  # Middle value is wrong type
                    test_data[req_col] = dummy_data
                else:
                    # For other columns, create appropriate dummy data
                    test_data[req_col] = self._create_dummy_data_for_column(
                        req_col, len(base_test_data)
                    )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

            validator = validator_class()
            result = validator.validate(gdf, check_stats=False)

            # Should fail due to wrong data type
            assert (
                not result.success
            ), f"Validation should fail when {col} has wrong type {type(wrong_value)}"
            assert len(result.errors) > 0

    def test_value_ranges(
        self,
        validator_class: Type[BaseValidator],
        range_specs: Dict[str, Dict[str, Any]],
        base_test_data: pd.DataFrame,
    ):
        """Test that the validator catches values outside expected ranges."""
        for col, spec in range_specs.items():
            min_val = spec.get("min")
            max_val = spec.get("max")

            if min_val is not None:
                # Test value below minimum
                test_data = self._create_test_data_with_value(
                    base_test_data, col, min_val - 1, range_specs
                )
                gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

                validator = validator_class()
                result = validator.validate(gdf, check_stats=False)

                # Should fail due to value below minimum
                assert (
                    not result.success
                ), f"Validation should fail when {col} is below minimum {min_val}"
                assert len(result.errors) > 0

            if max_val is not None:
                # Test value above maximum
                test_data = self._create_test_data_with_value(
                    base_test_data, col, max_val + 1, range_specs
                )
                gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

                validator = validator_class()
                result = validator.validate(gdf, check_stats=False)

                # Should fail due to value above maximum
                assert (
                    not result.success
                ), f"Validation should fail when {col} is above maximum {max_val}"
                assert len(result.errors) > 0

    def test_opa_id_validation(
        self,
        validator_class: Type[BaseValidator],
        valid_data_func: Callable,
        base_test_data: pd.DataFrame,
    ):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        # Test duplicate OPA IDs
        test_data = valid_data_func(base_test_data)
        test_data["opa_id"] = ["123", "123", "456"]  # Duplicate OPA ID
        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

        validator = validator_class()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to duplicate OPA IDs
        assert not result.success, "Validation should fail with duplicate OPA IDs"
        assert len(result.errors) > 0

        # Test non-string OPA ID
        test_data = valid_data_func(base_test_data)
        test_data["opa_id"] = ["123", 456, "789"]  # Non-string OPA ID
        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

        validator = validator_class()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to non-string OPA ID
        assert not result.success, "Validation should fail with non-string OPA ID"
        assert len(result.errors) > 0

        # Test null OPA ID
        test_data = valid_data_func(base_test_data)
        test_data["opa_id"] = ["123", None, "789"]  # Null OPA ID
        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

        validator = validator_class()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to null OPA ID
        assert not result.success, "Validation should fail with null OPA ID"
        assert len(result.errors) > 0

    def test_empty_dataframe(
        self, validator_class: Type[BaseValidator], empty_dataframe: pd.DataFrame
    ):
        """Test that the validator handles empty dataframes correctly."""
        gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

        validator = validator_class()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to missing required columns in empty dataframe
        assert not result.success, "Validation should fail with empty dataframe"
        assert len(result.errors) > 0

    def _create_test_data_with_value(
        self,
        base_test_data: pd.DataFrame,
        target_col: str,
        target_value: Any,
        column_specs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, List[Any]]:
        """Helper method to create test data with a specific value in a target column."""
        test_data = {}
        for col in column_specs.keys():
            if col == "opa_id":
                test_data[col] = base_test_data["opa_id"]
            elif col == "geometry":
                test_data[col] = base_test_data["geometry"]
            elif col == target_col:
                # Add target value to this column
                dummy_data = self._create_dummy_data_for_column(
                    col, len(base_test_data)
                )
                dummy_data[1] = target_value  # Middle value is target
                test_data[col] = dummy_data
            else:
                # For other columns, create appropriate dummy data
                test_data[col] = self._create_dummy_data_for_column(
                    col, len(base_test_data)
                )

        # Always include geometry column from base_test_data
        test_data["geometry"] = base_test_data["geometry"]

        return test_data

    def _create_dummy_data_for_column(self, col: str, length: int) -> List[Any]:
        """Helper method to create appropriate dummy data for a given column."""
        # Handle delinquencies-specific columns
        if col == "num_years_owed":
            return pd.Series([5, 10, 15], dtype="Int64")[:length].tolist()
        elif col in ["total_due", "total_assessment", "most_recent_year_owed"]:
            # These are object dtype due to "NA" strings
            if col == "total_due":
                return [1000.0, 5000.0, 10000.0][:length]
            elif col == "total_assessment":
                return [50000.0, 100000.0, 200000.0][:length]
            elif col == "most_recent_year_owed":
                return [2020, 2021, 2022][:length]
        elif col in ["is_actionable", "sheriff_sale", "payment_agreement"]:
            # These are object dtype string fields
            if col == "is_actionable":
                return ["true", "false", "true"][:length]
            elif col == "sheriff_sale":
                return ["N", "Y", "N"][:length]
            elif col == "payment_agreement":
                return ["false", "true", "false"][:length]

        # Default fallback for unknown columns
        return [0] * length
