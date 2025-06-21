import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.nbhoods import NeighborhoodsOutputValidator


def test_nbhoods_validator_schema_valid_data():
    """Test that the validator accepts valid data."""
    # Create valid test data
    test_data = pd.DataFrame(
        {
            "opa_id": ["test_1", "test_2", "test_3"],
            "neighborhood": ["Center City", "Fishtown", "Northern Liberties"],
            "geometry": [Point(-75.089, 40.033) for _ in range(3)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_nbhoods_validator_schema_edge_cases():
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": ["test_1", "test_2"],
            # Missing neighborhood column
            "geometry": [Point(-75.089, 40.033) for _ in range(2)],
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
            "opa_id": ["test_1", "test_2"],
            "neighborhood": ["Center City", None],  # Null value
            "geometry": [Point(-75.089, 40.033) for _ in range(2)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null neighborhood values
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_row_level_validation():
    """Test row-level validation that works with any dataset size."""
    # Test with small dataset (should pass row-level validation)
    test_data = pd.DataFrame(
        {
            "opa_id": ["test_1", "test_2"],
            "neighborhood": ["Center City", "Fishtown"],
            "geometry": [Point(-75.089, 40.033) for _ in range(2)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_nbhoods_validator_missing_required_columns():
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "neighborhood": ["Center City", "Fishtown"],
            "geometry": [Point(-75.089, 40.033) for _ in range(2)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_non_string_neighborhood():
    """Test that the validator catches non-string neighborhood values."""
    # Test with non-string neighborhood values
    test_data = pd.DataFrame(
        {
            "opa_id": ["test_1", "test_2"],
            "neighborhood": ["Center City", 123],  # Non-string value
            "geometry": [Point(-75.089, 40.033) for _ in range(2)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string neighborhood values
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_empty_dataframe():
    """Test that the validator handles empty dataframes correctly."""
    # Test with empty dataframe
    test_data = pd.DataFrame(columns=["opa_id", "neighborhood", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_small_dataset_statistical_checks():
    """Test that statistical checks are skipped for small datasets."""
    # Test with small dataset (less than threshold)
    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i}" for i in range(50)],  # Only 50 records
            "neighborhood": [
                f"Neighborhood_{i % 10}" for i in range(50)
            ],  # Only 10 neighborhoods
            "geometry": [Point(-75.089, 40.033) for _ in range(50)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass because statistical checks are skipped for small datasets
    assert result.success
    assert len(result.errors) == 0


def test_nbhoods_validator_wrong_neighborhood_count():
    """Test that the validator catches wrong number of unique neighborhoods."""
    # Create data with only 10 neighborhoods instead of ~160
    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i}" for i in range(200)],
            "neighborhood": [
                f"Neighborhood_{i % 10}" for i in range(200)
            ],  # Only 10 neighborhoods
            "geometry": [Point(-75.089, 40.033) for _ in range(200)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to wrong neighborhood count
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_too_many_neighborhoods():
    """Test that the validator catches too many unique neighborhoods."""
    # Create data with 200 neighborhoods (more than expected ~160)
    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i}" for i in range(200)],
            "neighborhood": [
                f"Neighborhood_{i}" for i in range(200)
            ],  # 200 unique neighborhoods
            "geometry": [Point(-75.089, 40.033) for _ in range(200)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too many neighborhoods
    assert not result.success
    assert len(result.errors) > 0


def test_nbhoods_validator_correct_neighborhood_count():
    """Test that the validator accepts correct number of unique neighborhoods."""
    # Create data with 160 neighborhoods (within expected range)
    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i}" for i in range(200)],
            "neighborhood": [
                f"Neighborhood_{i % 160}" for i in range(200)
            ],  # 160 unique neighborhoods
            "geometry": [Point(-75.089, 40.033) for _ in range(200)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = NeighborhoodsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass with correct neighborhood count
    assert result.success
    assert len(result.errors) == 0
