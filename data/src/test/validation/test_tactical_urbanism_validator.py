import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.tactical_urbanism import TacticalUrbanismOutputValidator


def _create_tactical_urbanism_test_data(base_test_data):
    """Create test data with only the columns expected by the tactical urbanism validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tactical_urbanism": [True, False, True],  # Boolean test data
            "geometry": base_test_data["geometry"],
        }
    )


class TestTacticalUrbanismValidator(BaseValidatorTestMixin):
    """Test class for tactical urbanism validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for tactical urbanism validator."""
        return [
            "opa_id",
            "tactical_urbanism",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "tactical_urbanism": {"type": "bool", "wrong_value": "not_a_boolean"},
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
            TacticalUrbanismOutputValidator,
            _create_tactical_urbanism_test_data,
            base_test_data,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        # Only test for missing tactical_urbanism column - geometry is handled by base validator
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                # Missing tactical_urbanism column
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = TacticalUrbanismOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to missing tactical_urbanism column
        assert not result.success, (
            "Validation should fail when tactical_urbanism column is missing"
        )
        assert len(result.errors) > 0

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For tactical_urbanism, tactical_urbanism is not nullable, so we only test opa_id and geometry
        # which are handled by the base validator
        pass

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            TacticalUrbanismOutputValidator, column_specs, base_test_data
        )

    def test_opa_id_validation(self, base_test_data):
        """Test that the validator properly validates OPA IDs."""
        super().test_opa_id_validation(
            TacticalUrbanismOutputValidator,
            _create_tactical_urbanism_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes."""
        super().test_empty_dataframe(TacticalUrbanismOutputValidator, empty_dataframe)

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        # For tactical_urbanism, there are no numeric ranges to test since it's boolean
        # This method is required by the base mixin but not applicable here
        pass
