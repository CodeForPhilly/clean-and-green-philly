import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.unsafe_buildings import UnsafeBuildingsOutputValidator


def _create_unsafe_buildings_test_data(base_test_data):
    """Create test data with only the columns expected by the unsafe buildings validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "unsafe_building": [True, False, True],  # Valid boolean values
            "geometry": base_test_data["geometry"],
        }
    )


def test_unsafe_buildings_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_unsafe_buildings_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_unsafe_buildings_validator_schema_edge_cases(base_test_data):
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing unsafe_building column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing unsafe_building column
    assert not result.success
    assert len(result.errors) > 0

    # Test with null unsafe_building values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "unsafe_building": [
                True,
                None,
                False,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null unsafe_building values
    assert not result.success
    assert len(result.errors) > 0


def test_unsafe_buildings_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_unsafe_buildings_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_unsafe_buildings_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "unsafe_building": [True, False, True],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0


def test_unsafe_buildings_validator_non_boolean_unsafe_building(base_test_data):
    """Test that the validator catches non-boolean unsafe_building values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "unsafe_building": [
                True,
                "maybe",
                False,
            ],  # Non-boolean value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-boolean unsafe_building values
    assert not result.success
    assert len(result.errors) > 0


def test_unsafe_buildings_validator_null_unsafe_building_values(base_test_data):
    """Test that the validator catches null values in unsafe_building column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "unsafe_building": [
                True,
                None,
                False,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null values in unsafe_building column
    assert not result.success
    assert len(result.errors) > 0


def test_unsafe_buildings_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes correctly."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_unsafe_buildings_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351243200", "212525650"],  # Duplicate OPA ID
            "unsafe_building": [True, False, True],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.089, 40.033),  # Same geometry for duplicate
                Point(-75.244, 40.072),
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = UnsafeBuildingsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs
    assert not result.success
    assert len(result.errors) > 0
