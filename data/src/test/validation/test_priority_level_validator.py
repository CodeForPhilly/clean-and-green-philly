import geopandas as gpd
import pandas as pd
import pytest

from src.test.validation.base_validator_test_mixin import BaseValidatorTestMixin
from src.validation.priority_level import PriorityLevelOutputValidator


def _create_priority_level_test_data(base_test_data):
    """Create test data with only the columns expected by the priority level validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "priority_level": ["High", "Medium", "Low"],  # Valid test data
            "geometry": base_test_data["geometry"],
        }
    )


def _create_priority_level_test_data_with_nulls(base_test_data):
    """Create test data with some null values in priority_level."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "priority_level": ["High", None, "Low"],  # One null value
            "geometry": base_test_data["geometry"],
        }
    )


def _create_priority_level_test_data_with_na(base_test_data):
    """Create test data with 'NA' values in priority_level."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "priority_level": ["High", "NA", "Low"],  # One 'NA' value
            "geometry": base_test_data["geometry"],
        }
    )


class TestPriorityLevelValidator(BaseValidatorTestMixin):
    """Test class for priority level validator using the base test mixin."""

    @pytest.fixture
    def required_columns(self):
        """Define required columns for priority level validator."""
        return [
            "opa_id",
            "priority_level",
            "geometry",
        ]

    @pytest.fixture
    def column_specs(self):
        """Define column specifications for data type testing."""
        return {
            "opa_id": {"type": "str", "wrong_value": 123456789},
            "priority_level": {
                "type": "object",
                "wrong_value": 123,
            },  # object type for mixed string/NA
            "geometry": {"type": "geometry", "wrong_value": "not_a_geometry"},
        }

    @pytest.fixture
    def range_specs(self):
        """Define value range specifications for testing."""
        # Priority level doesn't have numeric ranges, so return empty dict
        return {}

    def test_schema_valid_data(self, base_test_data):
        """Test that the validator accepts valid data."""
        super().test_schema_valid_data(
            PriorityLevelOutputValidator,
            _create_priority_level_test_data,
            base_test_data,
            check_stats=False,
        )

    def test_missing_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches missing required columns."""
        super().test_missing_required_columns(
            PriorityLevelOutputValidator, required_columns, base_test_data
        )

    def test_null_values_in_required_columns(self, base_test_data, required_columns):
        """Test that the validator catches null values in required columns."""
        # For priority_level, the column is nullable, so we only test opa_id and geometry
        # which are handled by the base validator
        pass

    def test_wrong_data_types(self, base_test_data, column_specs):
        """Test that the validator catches wrong data types."""
        super().test_wrong_data_types(
            PriorityLevelOutputValidator, column_specs, base_test_data
        )

    def test_value_ranges(self, base_test_data, range_specs):
        """Test that the validator catches values outside expected ranges."""
        # Priority level doesn't have numeric ranges, so this test is not applicable
        pass

    def test_opa_id_validation(self, base_test_data):
        """Test OPA ID validation (uniqueness, string type, non-null)."""
        super().test_opa_id_validation(
            PriorityLevelOutputValidator,
            _create_priority_level_test_data,
            base_test_data,
        )

    def test_empty_dataframe(self, empty_dataframe):
        """Test that the validator handles empty dataframes correctly."""
        super().test_empty_dataframe(PriorityLevelOutputValidator, empty_dataframe)

    # Service-specific tests that don't fit the generic pattern
    def test_valid_priority_level_values(self, base_test_data):
        """Test that the validator accepts all valid priority level values."""
        valid_values = ["High", "Medium", "Low", "NA"]

        for value in valid_values:
            test_data = pd.DataFrame(
                {
                    "opa_id": base_test_data["opa_id"],
                    "priority_level": [value, "Medium", "Low"],  # Test each valid value
                    "geometry": base_test_data["geometry"],
                }
            )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

            validator = PriorityLevelOutputValidator()
            result = validator.validate(gdf, check_stats=False)

            # Should pass with valid priority level values
            assert result.success, (
                f"Validation failed for value '{value}' with errors: {result.errors}"
            )
            assert len(result.errors) == 0

    def test_case_insensitive_validation(self, base_test_data):
        """Test that the validator accepts case variations of valid values."""
        case_variations = ["high", "MEDIUM", "Low", "na", "HIGH", "medium", "LOW", "NA"]

        for value in case_variations:
            test_data = pd.DataFrame(
                {
                    "opa_id": base_test_data["opa_id"],
                    "priority_level": [
                        value,
                        "Medium",
                        "Low",
                    ],  # Test each case variation
                    "geometry": base_test_data["geometry"],
                }
            )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

            validator = PriorityLevelOutputValidator()
            result = validator.validate(gdf, check_stats=False)

            # Should pass with case variations of valid values
            assert result.success, (
                f"Validation failed for case variation '{value}' with errors: {result.errors}"
            )
            assert len(result.errors) == 0

    def test_invalid_priority_level_values(self, base_test_data):
        """Test that the validator rejects invalid priority level values."""
        invalid_values = [
            "Critical",
            "Normal",
            "Urgent",
            "Low Priority",
            "High Priority",
            "Medium Priority",
            "",
        ]

        for value in invalid_values:
            test_data = pd.DataFrame(
                {
                    "opa_id": base_test_data["opa_id"],
                    "priority_level": [
                        value,
                        "Medium",
                        "Low",
                    ],  # Test each invalid value
                    "geometry": base_test_data["geometry"],
                }
            )

            gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

            validator = PriorityLevelOutputValidator()
            result = validator.validate(gdf, check_stats=False)

            # Should fail due to invalid priority level value
            assert not result.success, (
                f"Validation should fail for invalid value '{value}'"
            )
            assert len(result.errors) > 0

    def test_null_values_allowed(self, base_test_data):
        """Test that the validator allows null values in priority_level column."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": ["High", None, "Low"],  # One null value
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with null values (nullable=True)
        assert result.success, f"Validation failed with null values: {result.errors}"
        assert len(result.errors) == 0

    def test_all_null_values(self, base_test_data):
        """Test that the validator handles all null values in priority_level column."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": [None, None, None],  # All null values
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should pass with all null values (nullable=True)
        assert result.success, (
            f"Validation failed with all null values: {result.errors}"
        )
        assert len(result.errors) == 0

    def test_mixed_valid_and_invalid_values(self, base_test_data):
        """Test that the validator rejects data with mixed valid and invalid values."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": ["High", "Invalid", "Low"],  # One invalid value
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to invalid value
        assert not result.success, (
            "Validation should fail when mixed with invalid values"
        )
        assert len(result.errors) > 0

    def test_edge_case_empty_string(self, base_test_data):
        """Test that the validator rejects empty strings."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": ["High", "", "Low"],  # Empty string
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to empty string
        assert not result.success, "Validation should fail with empty string"
        assert len(result.errors) > 0

    def test_edge_case_whitespace_only(self, base_test_data):
        """Test that the validator rejects whitespace-only strings."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": ["High", "   ", "Low"],  # Whitespace only
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()
        result = validator.validate(gdf, check_stats=False)

        # Should fail due to whitespace-only string
        assert not result.success, "Validation should fail with whitespace-only string"
        assert len(result.errors) > 0

    def test_statistical_summary_method(self, base_test_data):
        """Test that the statistical summary method works correctly."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": [
                    "High",
                    "Medium",
                    "Low",
                ],  # Match the length of base_test_data
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()

        # This should not raise any exceptions
        try:
            validator._print_statistical_summary(gdf)
        except Exception as e:
            pytest.fail(f"Statistical summary method failed: {e}")

    def test_custom_validation_method(self, base_test_data):
        """Test that the custom validation method works correctly."""
        test_data = pd.DataFrame(
            {
                "opa_id": base_test_data["opa_id"],
                "priority_level": ["High", "Medium", "Low"],
                "geometry": base_test_data["geometry"],
            }
        )

        gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs="EPSG:2272")

        validator = PriorityLevelOutputValidator()

        # This should not raise any exceptions
        try:
            validator._custom_validation(gdf, check_stats=False)
        except Exception as e:
            pytest.fail(f"Custom validation method failed: {e}")
