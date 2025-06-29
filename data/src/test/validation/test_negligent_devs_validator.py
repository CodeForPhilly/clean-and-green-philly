"""
Tests for the negligent devs validator using the base test mixin.

This demonstrates how to use the BaseValidatorTestMixin to create comprehensive
validator tests with minimal repetitive code.
"""

import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.negligent_devs import NegligentDevsOutputValidator


def _create_negligent_devs_test_data(base_test_data):
    """Create test data with only the columns expected by the negligent devs validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "negligent_dev": [False, False, True],  # Boolean values
            "n_total_properties_owned": [50, 60, 80],  # Values closer to mean ~67
            "n_vacant_properties_owned": [15, 18, 25],  # Values closer to mean ~19
            "avg_violations_per_property": [
                0.05,
                0.07,
                0.09,
            ],  # Values closer to mean ~0.069
            "geometry": base_test_data["geometry"],
        }
    )


class TestNegligentDevsValidator(BaseValidatorTestMixin):
    """Test class for negligent devs validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for negligent devs validator."""
        return [
            "opa_id",
            "negligent_dev",
            "n_total_properties_owned",
            "n_vacant_properties_owned",
            "avg_violations_per_property",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "negligent_dev": {"type": "bool", "wrong_value": "not_a_bool"},
            "n_total_properties_owned": {"type": "int", "wrong_value": "not_a_number"},
            "n_vacant_properties_owned": {"type": "int", "wrong_value": "not_a_number"},
            "avg_violations_per_property": {
                "type": "float",
                "wrong_value": "not_a_number",
            },
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        return {
            "n_total_properties_owned": {"min": 0, "max": 5059},
            "n_vacant_properties_owned": {"min": 0, "max": 1296},
            "avg_violations_per_property": {"min": 0.0, "max": 17.0},
        }

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            NegligentDevsOutputValidator,
            _create_negligent_devs_test_data,
            base_test_data,
            check_stats=False,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        super().test_missing_required_columns(
            NegligentDevsOutputValidator, required_columns, base_test_data
        )

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        super().test_null_values_in_required_columns(
            NegligentDevsOutputValidator, required_columns, base_test_data
        )

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            NegligentDevsOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        super().test_value_ranges(
            NegligentDevsOutputValidator, range_specs, base_test_data
        )

    def test_opa_id_validation(self, base_test_data):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        super().test_opa_id_validation(
            NegligentDevsOutputValidator,
            _create_negligent_devs_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes correctly."""
        super().test_empty_dataframe(NegligentDevsOutputValidator, empty_dataframe)

    # Service-specific tests for negligent devs validation
    def test_negligent_dev_boolean_values(self, base_test_data):
        """Test that negligent_dev must be boolean values."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, "maybe", True],  # Invalid value in middle
                "n_total_properties_owned": [50, 60, 80],  # Values closer to mean ~67
                "n_vacant_properties_owned": [15, 18, 25],  # Values closer to mean ~19
                "avg_violations_per_property": [
                    0.05,
                    0.07,
                    0.09,
                ],  # Values closer to mean ~0.069
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to non-boolean value in negligent_dev
        assert not result.success, (
            "Validation should fail when negligent_dev has non-boolean value"
        )
        assert len(result.errors) > 0

    def test_property_counts_non_negative(self, base_test_data):
        """Test that property count columns must be non-negative."""
        # Test negative n_total_properties_owned
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, True],
                "n_total_properties_owned": [50, -1, 80],  # Negative value
                "n_vacant_properties_owned": [15, 18, 25],
                "avg_violations_per_property": [0.05, 0.07, 0.09],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to negative property count
        assert not result.success, (
            "Validation should fail when n_total_properties_owned is negative"
        )
        assert len(result.errors) > 0

        # Test negative n_vacant_properties_owned
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, True],
                "n_total_properties_owned": [50, 60, 80],
                "n_vacant_properties_owned": [15, -1, 25],  # Negative value
                "avg_violations_per_property": [0.05, 0.07, 0.09],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to negative vacant property count
        assert not result.success, (
            "Validation should fail when n_vacant_properties_owned is negative"
        )
        assert len(result.errors) > 0

    def test_violations_per_property_non_negative(self, base_test_data):
        """Test that avg_violations_per_property must be non-negative."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, True],
                "n_total_properties_owned": [50, 60, 80],
                "n_vacant_properties_owned": [15, 18, 25],
                "avg_violations_per_property": [0.05, -0.07, 0.09],  # Negative value
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to negative violations per property
        assert not result.success, (
            "Validation should fail when avg_violations_per_property is negative"
        )
        assert len(result.errors) > 0

    def test_vacant_properties_leq_total_properties(self, base_test_data):
        """Test that n_vacant_properties_owned <= n_total_properties_owned."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, True],
                "n_total_properties_owned": [50, 60, 80],
                "n_vacant_properties_owned": [15, 70, 25],  # 70 > 60 (total properties)
                "avg_violations_per_property": [0.05, 0.07, 0.09],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to vacant properties > total properties
        assert not result.success, (
            "Validation should fail when vacant properties > total properties"
        )
        assert len(result.errors) > 0

    def test_edge_case_values(self, base_test_data):
        """Test edge case values that should pass validation."""
        # Test with maximum allowed values
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, True],
                "n_total_properties_owned": [
                    0,
                    6000,
                    3000,
                ],  # Min, max, and middle values
                "n_vacant_properties_owned": [
                    0,
                    1300,
                    650,
                ],  # Min, max, and middle values
                "avg_violations_per_property": [
                    0.0,
                    17.0,
                    8.5,
                ],  # Min, max, and middle values
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with edge case values
        assert result.success, (
            f"Validation failed with edge case values: {result.errors}"
        )
        assert len(result.errors) == 0

    def test_all_false_negligent_dev(self, base_test_data):
        """Test that validator accepts data where all negligent_dev values are False."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [False, False, False],  # All False
                "n_total_properties_owned": [50, 60, 80],
                "n_vacant_properties_owned": [15, 18, 25],
                "avg_violations_per_property": [0.05, 0.07, 0.09],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with all False negligent_dev values
        assert result.success, (
            f"Validation failed with all False negligent_dev values: {result.errors}"
        )
        assert len(result.errors) == 0

    def test_all_true_negligent_dev(self, base_test_data):
        """Test that validator accepts data where all negligent_dev values are True."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "negligent_dev": [True, True, True],  # All True
                "n_total_properties_owned": [50, 60, 80],
                "n_vacant_properties_owned": [15, 18, 25],
                "avg_violations_per_property": [0.05, 0.07, 0.09],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = NegligentDevsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with all True negligent_dev values
        assert result.success, (
            f"Validation failed with all True negligent_dev values: {result.errors}"
        )
        assert len(result.errors) == 0
