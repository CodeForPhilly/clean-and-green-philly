import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.nbhoods import NeighborhoodsOutputValidator


def _create_neighborhoods_test_data(base_test_data):
    """Create test data with only the columns expected by the neighborhoods validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "neighborhood": ["Center City", "Fishtown", "Northern Liberties"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_nbhoods_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_neighborhoods_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_nbhoods_validator_schema_edge_cases(base_test_data):
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing neighborhood column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing neighborhood column
    assert not result.success
    assert len(result.errors) > 0

    # Test with null neighborhood values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "neighborhood": [
                "Center City",
                None,
                "Northern Liberties",
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null neighborhood values
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_neighborhoods_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_nbhoods_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "neighborhood": ["Center City", "Fishtown", "Northern Liberties"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_non_string_neighborhood(base_test_data):
    """Test that the validator catches non-string neighborhood values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "neighborhood": [
                "Center City",
                123,
                "Northern Liberties",
            ],  # Non-string value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string neighborhood values
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes correctly."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0
