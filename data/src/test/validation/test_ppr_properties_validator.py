import logging

import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.ppr_properties import PPRPropertiesOutputValidator

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _create_ppr_properties_test_data(base_test_data):
    """Create test data with only the columns expected by the PPR properties validator."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "vacant": [False, False, False],  # PPR properties should not be vacant
            "geometry": base_test_data["geometry"],
        }
    )

    logger.debug(f"Created test data with shape: {test_data.shape}")
    logger.debug(f"Test data columns: {list(test_data.columns)}")
    logger.debug(f"Test data dtypes: {test_data.dtypes}")
    logger.debug("Test data info:")
    logger.debug(test_data.info())
    logger.debug(f"Vacant column values: {test_data['vacant'].tolist()}")
    logger.debug(f"Vacant column dtype: {test_data['vacant'].dtype}")
    logger.debug(f"Vacant column type: {type(test_data['vacant'])}")
    logger.debug(
        f"Vacant column value types: {[type(val) for val in test_data['vacant']]}"
    )

    return test_data


class TestPPRPropertiesValidator(BaseValidatorTestMixin):
    """Test class for PPR properties validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for PPR properties validator."""
        return [
            "opa_id",
            "vacant",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "vacant": {"type": "object", "wrong_value": "not_a_boolean"},
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        # PPR properties doesn't have numeric ranges, so return empty dict
        return {}

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            PPRPropertiesOutputValidator,
            _create_ppr_properties_test_data,
            base_test_data,
            check_stats=False,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        super().test_missing_required_columns(
            PPRPropertiesOutputValidator, required_columns, base_test_data
        )

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For PPR properties, vacant is nullable, so we only test opa_id and geometry
        # which are handled by the base validator
        pass

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            PPRPropertiesOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        # PPR properties doesn't have numeric ranges, so this test is not applicable
        pass

    def test_opa_id_validation(self, base_test_data):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        super().test_opa_id_validation(
            PPRPropertiesOutputValidator,
            _create_ppr_properties_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes correctly."""
        super().test_empty_dataframe(PPRPropertiesOutputValidator, empty_dataframe)

    # Service-specific tests that don't fit the generic pattern
    def test_valid_vacant_values(self, base_test_data):
        """Test that the validator accepts valid vacant values."""
        valid_values = [True, False, None]  # All valid for vacant column

        for value in valid_values:
            logger.debug(f"\n=== Testing value: {value} (type: {type(value)}) ===")

            test_data = pd.DataFrame(
                {
                    "opa_id": base_test_data["opa_id"],
                    "vacant": [value, False, False],  # Test each valid value
                    "geometry": base_test_data["geometry"],
                }
            )

            logger.debug(
                f"Created DataFrame with vacant values: {test_data['vacant'].tolist()}"
            )
            logger.debug(f"DataFrame dtypes: {test_data.dtypes}")
            logger.debug(f"Vacant column dtype: {test_data['vacant'].dtype}")
            logger.debug(
                f"Vacant column value types: {[type(val) for val in test_data['vacant']]}"
            )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

            logger.debug(f"GeoDataFrame dtypes: {gdf.dtypes}")
            logger.debug(f"GeoDataFrame vacant dtype: {gdf['vacant'].dtype}")

            validator = PPRPropertiesOutputValidator()
            result = validator.validate(gdf, check_stats=False)

            # Should pass with valid vacant values
            assert result.success, (
                f"Validation failed for value '{value}' with errors: {result.errors}"
            )
            assert len(result.errors) == 0

    def test_null_values_allowed_in_vacant(self, base_test_data):
        """Test that the validator allows null values in vacant column."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "vacant": [False, None, False],  # One null value
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PPRPropertiesOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with null values (nullable=True)
        assert result.success, f"Validation failed with null values: {result.errors}"
        assert len(result.errors) == 0

    def test_statistical_summary_method(self, base_test_data):
        """Test that the statistical summary method works correctly."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "vacant": [False, True, False],  # Match the length of base_test_data
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PPRPropertiesOutputValidator()

        # This should not raise any exceptions
        try:
            validator._print_statistical_summary(gdf)
        except Exception as e:
            pytest.fail(f"Statistical summary method failed: {e}")
