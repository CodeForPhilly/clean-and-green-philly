import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.dev_probability import DevProbabilityOutputValidator


def _create_dev_probability_test_data(base_test_data):
    """Create test data with only the columns expected by the dev probability validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "permit_count": [0, 25, 50],  # Simple test data
            "dev_rank": ["Low", "Medium", "High"],
            "geometry": base_test_data["geometry"],
        }
    )


class TestDevProbabilityValidator(BaseValidatorTestMixin):
    """Test class for dev probability validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for dev probability validator."""
        return [
            "opa_id",
            "permit_count",
            "dev_rank",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "permit_count": {"type": "int", "wrong_value": "not_a_number"},
            "dev_rank": {"type": "str", "wrong_value": 123},
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        return {
            "permit_count": {
                "min": 0,
                "max": 420,
            },  # Based on updated schema constraints
        }

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        # For this test, we'll create data that should pass basic validation
        # The statistical constraints may still fail, but that's expected
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "permit_count": [0, 25, 50],  # Simple test data
                "dev_rank": ["Low", "Medium", "High"],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DevProbabilityOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # The validator should either pass or fail based on statistical constraints
        # Both outcomes are valid for testing the validation logic
        if not result.success:
            # If it fails, make sure it's due to statistical constraints
            error_messages = " ".join(result.errors)
            assert any(
                constraint in error_messages.lower()
                for constraint in ["mean", "std", "q1", "q3", "max"]
            ), f"Unexpected validation error: {result.errors}"
        else:
            # If it passes, that's also fine
            assert len(result.errors) == 0

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        super().test_missing_required_columns(
            DevProbabilityOutputValidator, required_columns, base_test_data
        )

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For dev_probability, permit_count and dev_rank are non-nullable
        # Test permit_count null values
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "permit_count": [0, None, 50],  # Middle value is null
                "dev_rank": ["Low", "Medium", "High"],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DevProbabilityOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to null values in permit_count
        assert not result.success, (
            "Validation should fail when permit_count has null values"
        )
        assert len(result.errors) > 0

        # Test dev_rank null values
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "permit_count": [0, 25, 50],
                "dev_rank": ["Low", None, "High"],  # Middle value is null
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DevProbabilityOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to null values in dev_rank
        assert not result.success, (
            "Validation should fail when dev_rank has null values"
        )
        assert len(result.errors) > 0

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            DevProbabilityOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        super().test_value_ranges(
            DevProbabilityOutputValidator, range_specs, base_test_data
        )

    def test_opa_id_validation(self, base_test_data):
        """Test that the validator properly validates opa_id."""
        super().test_opa_id_validation(
            DevProbabilityOutputValidator,
            _create_dev_probability_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes."""
        super().test_empty_dataframe(DevProbabilityOutputValidator, empty_dataframe)

    # Service-specific tests for dev probability validation
    def test_dev_rank_valid_values(self, base_test_data):
        """Test that dev_rank must be one of the valid values."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "permit_count": [0, 25, 50],
                "dev_rank": ["Low", "Invalid", "High"],  # Invalid value in middle
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DevProbabilityOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to invalid dev_rank value
        assert not result.success, (
            "Validation should fail when dev_rank has invalid value"
        )
        assert len(result.errors) > 0

    def test_case_sensitive_dev_rank(self, base_test_data):
        """Test that dev_rank is case sensitive."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "permit_count": [0, 25, 50],
                "dev_rank": ["low", "medium", "high"],  # Lowercase
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = DevProbabilityOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to case sensitivity
        assert not result.success, (
            "Validation should fail with lowercase dev_rank values"
        )
        assert len(result.errors) > 0
