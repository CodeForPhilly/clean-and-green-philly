import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.conservatorship import ConservatorshipOutputValidator


def _create_conservatorship_test_data(base_test_data):
    """Create test data with only the columns expected by the conservatorship validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "conservatorship": [True, False, True],  # Boolean test data
            "geometry": base_test_data["geometry"],
        }
    )


def _create_conservatorship_test_data_with_nulls(base_test_data):
    """Create test data with some null values in conservatorship."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "conservatorship": [True, None, False],  # One null value
            "geometry": base_test_data["geometry"],
        }
    )


class TestConservatorshipValidator(BaseValidatorTestMixin):
    """Test class for conservatorship validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for conservatorship validator."""
        return [
            "opa_id",
            "conservatorship",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "conservatorship": {"type": "bool", "wrong_value": "not_a_boolean"},
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        return {
            # Boolean columns don't have numeric ranges
        }

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            ConservatorshipOutputValidator,
            _create_conservatorship_test_data,
            base_test_data,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        # Only test for missing conservatorship column - geometry is handled by base validator
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                # Missing conservatorship column
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = ConservatorshipOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to missing conservatorship column
        assert not result.success, (
            "Validation should fail when conservatorship column is missing"
        )
        assert len(result.errors) > 0

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For conservatorship, conservatorship is not nullable, so we only test opa_id and geometry
        # which are handled by the base validator
        pass

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            ConservatorshipOutputValidator, column_specs, base_test_data
        )

    def test_opa_id_validation(self, base_test_data):
        """Test that the validator properly validates OPA IDs."""
        super().test_opa_id_validation(
            ConservatorshipOutputValidator,
            _create_conservatorship_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes."""
        super().test_empty_dataframe(ConservatorshipOutputValidator, empty_dataframe)

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        # For conservatorship, there are no numeric ranges to test since it's boolean
        # This method is required by the base mixin but not applicable here
        pass
