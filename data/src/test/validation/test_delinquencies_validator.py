"""
Tests for the delinquencies validator using the base test mixin.

This demonstrates how to use the BaseValidatorTestMixin to create comprehensive
validator tests with minimal repetitive code.
"""

import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.delinquencies import DelinquenciesOutputValidator


def _create_delinquencies_test_data(base_test_data):
    """Create test data with only the columns expected by the delinquencies validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "num_years_owed": pd.Series(
                [5, 10, 15], dtype="Int64"
            ),  # Explicit Int64 dtype
            "total_due": [
                1000.0,
                5000.0,
                10000.0,
            ],  # Will be object dtype due to mixed types in actual data
            "total_assessment": [
                50000.0,
                100000.0,
                200000.0,
            ],  # Will be object dtype due to mixed types in actual data
            "is_actionable": ["true", "false", "true"],  # String values
            "sheriff_sale": ["N", "Y", "N"],  # String values
            "payment_agreement": ["false", "true", "false"],  # String values
            "most_recent_year_owed": [
                2020,
                2021,
                2022,
            ],  # Will be object dtype due to mixed types in actual data
            "geometry": base_test_data["geometry"],
        }
    ).astype(
        {
            # Ensure these columns are object dtype to match schema expectations
            "total_due": "object",
            "total_assessment": "object",
            "most_recent_year_owed": "object",
        }
    )


class TestDelinquenciesValidator(BaseValidatorTestMixin):
    """Test class for delinquencies validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for delinquencies validator."""
        return [
            "opa_id",
            "num_years_owed",
            "total_due",
            "total_assessment",
            "is_actionable",
            "sheriff_sale",
            "payment_agreement",
            "most_recent_year_owed",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "num_years_owed": {"type": "Int64", "wrong_value": "not_a_number"},
            "total_due": {
                "type": "object",
                "wrong_value": "invalid_string",  # String that can't be converted to numeric
            },
            "total_assessment": {
                "type": "object",
                "wrong_value": "invalid_string",  # String that can't be converted to numeric
            },
            "is_actionable": {"type": "object", "wrong_value": 123},  # String field
            "sheriff_sale": {"type": "object", "wrong_value": 123},  # String field
            "payment_agreement": {"type": "object", "wrong_value": 123},  # String field
            "most_recent_year_owed": {
                "type": "object",
                "wrong_value": "invalid_year",  # String that can't be converted to int
            },
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        return {
            "num_years_owed": {"min": 1, "max": 45},
            "total_due": {"min": 0.01, "max": 1200000},
            "total_assessment": {"min": 0, "max": 140000000},
        }

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            DelinquenciesOutputValidator,
            _create_delinquencies_test_data,
            base_test_data,
            check_stats=False,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        super().test_missing_required_columns(
            DelinquenciesOutputValidator, required_columns, base_test_data
        )

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        super().test_null_values_in_required_columns(
            DelinquenciesOutputValidator, required_columns, base_test_data
        )

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            DelinquenciesOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        super().test_value_ranges(
            DelinquenciesOutputValidator, range_specs, base_test_data
        )

    def test_opa_id_validation(self, base_test_data):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        super().test_opa_id_validation(
            DelinquenciesOutputValidator,
            _create_delinquencies_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes correctly."""
        super().test_empty_dataframe(DelinquenciesOutputValidator, empty_dataframe)

    # Service-specific tests that don't fit the generic pattern
    def test_mixed_data_types_with_na_strings(self, base_test_data):
        """Test that the validator handles mixed data types with 'NA' strings correctly."""
        # Create test data with "NA" strings mixed with valid values (like the actual service)
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "num_years_owed": pd.Series(
                    [5, None, 15], dtype="Int64"
                ),  # Int64 with null
                "total_due": [
                    1000.0,
                    "NA",
                    10000.0,
                ],  # Mixed float/string (like actual service)
                "total_assessment": [
                    50000.0,
                    "NA",
                    200000.0,
                ],  # Mixed float/string (like actual service)
                "is_actionable": ["true", "NA", "true"],  # Mixed string
                "sheriff_sale": ["N", "NA", "N"],  # Mixed string
                "payment_agreement": ["false", "NA", "false"],  # Mixed string
                "most_recent_year_owed": [
                    2020,
                    "NA",
                    2022,
                ],  # Mixed int/string (like actual service)
                "geometry": base_test_data["geometry"],
            }
        ).astype(
            {
                # Ensure these columns are object dtype to match schema expectations
                "total_due": "object",
                "total_assessment": "object",
                "most_recent_year_owed": "object",
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DelinquenciesOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with mixed data types (this is expected behavior)
        assert (
            result.success
        ), f"Validation failed with mixed data types: {result.errors}"
        assert len(result.errors) == 0

    def test_edge_case_values(self, base_test_data):
        """Test edge case values that should pass validation."""
        # Test with maximum allowed values
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "num_years_owed": pd.Series(
                    [1, 45, 25], dtype="Int64"
                ),  # Min, max, and middle values
                "total_due": [0.01, 1200000.0, 5000.0],  # Min, max, and middle values
                "total_assessment": [
                    0.0,
                    140000000.0,
                    100000.0,
                ],  # Min, max, and middle values
                "is_actionable": ["true", "false", "true"],
                "sheriff_sale": ["Y", "N", "Y"],
                "payment_agreement": ["true", "false", "true"],
                "most_recent_year_owed": [2020, 2021, 2022],
                "geometry": base_test_data["geometry"],
            }
        ).astype(
            {
                # Ensure these columns are object dtype to match schema expectations
                "total_due": "object",
                "total_assessment": "object",
                "most_recent_year_owed": "object",
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DelinquenciesOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with edge case values
        assert (
            result.success
        ), f"Validation failed with edge case values: {result.errors}"
        assert len(result.errors) == 0
