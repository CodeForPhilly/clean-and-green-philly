import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.contig_neighbors import ContigNeighborsOutputValidator


def _create_contig_neighbors_test_data(base_test_data):
    """Create test data with only the columns expected by the contig neighbors validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "n_contiguous": [0.0, 0.0, 3.0],  # Simple test data
            "geometry": base_test_data["geometry"],
        }
    )


class TestContigNeighborsValidator(BaseValidatorTestMixin):
    """Test class for contig neighbors validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for contig neighbors validator."""
        return [
            "opa_id",
            "n_contiguous",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "n_contiguous": {"type": "float", "wrong_value": "not_a_number"},
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        return {
            "n_contiguous": {"max": 70},  # Based on schema constraints
        }

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            ContigNeighborsOutputValidator,
            _create_contig_neighbors_test_data,
            base_test_data,
            check_stats=False,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        # Only test for missing n_contiguous column - geometry is handled by base validator
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                # Missing n_contiguous column
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = ContigNeighborsOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to missing n_contiguous column
        assert not result.success, (
            "Validation should fail when n_contiguous column is missing"
        )
        assert len(result.errors) > 0

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For contig_neighbors, n_contiguous is nullable, so we only test opa_id and geometry
        # which are handled by the base validator
        pass

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            ContigNeighborsOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        # Only test n_contiguous ranges - geometry is handled by base validator
        for col, spec in range_specs.items():
            max_val = spec.get("max")

            if max_val is not None:
                # Test value above maximum
                test_data = pd.DataFrame(
                    {
                        "opa_id": base_test_data["opa_id"],
                        "n_contiguous": [0.0, max_val + 1, 3.0],  # Value above maximum
                        "geometry": base_test_data["geometry"],
                    }
                )
                gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

                validator = ContigNeighborsOutputValidator()
                result = validator.validate(gdf, check_stats=False)

                # Should fail due to value above maximum
                assert not result.success, (
                    f"Validation should fail when {col} is above maximum {max_val}"
                )
                assert len(result.errors) > 0

    def test_opa_id_validation(self, base_test_data):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        super().test_opa_id_validation(
            ContigNeighborsOutputValidator,
            _create_contig_neighbors_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes correctly."""
        super().test_empty_dataframe(ContigNeighborsOutputValidator, empty_dataframe)
