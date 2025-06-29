import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.tree_canopy import TreeCanopyOutputValidator


def _create_tree_canopy_test_data(base_test_data):
    """Create test data with only the columns expected by the tree canopy validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [0.1, 0.2, 0.3],  # Valid numeric values
            "geometry": base_test_data["geometry"],
        }
    )


def test_tree_canopy_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_tree_canopy_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_tree_canopy_validator_schema_edge_cases(base_test_data):
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing tree_canopy_gap column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing tree_canopy_gap column
    assert not result.success
    assert len(result.errors) > 0

    # Test with null tree_canopy_gap values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [
                0.1,
                None,
                0.3,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null tree_canopy_gap values
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_tree_canopy_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_tree_canopy_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "tree_canopy_gap": [0.1, 0.2, 0.3],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_non_numeric_tree_canopy_gap(base_test_data):
    """Test that the validator catches non-numeric tree_canopy_gap values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [
                0.1,
                "maybe",
                0.3,
            ],  # Non-numeric value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-numeric tree_canopy_gap values
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_null_tree_canopy_gap_values(base_test_data):
    """Test that the validator catches null values in tree_canopy_gap column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [
                0.1,
                None,
                0.3,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null values in tree_canopy_gap column
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_out_of_range_values(base_test_data):
    """Test that the validator catches values outside the expected range [0.0, 1.0]."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [
                0.1,
                1.5,  # Out of range (> 1.0)
                0.3,
            ],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to out-of-range values
    assert not result.success
    assert len(result.errors) > 0

    # Test with negative values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "tree_canopy_gap": [
                0.1,
                -0.1,  # Out of range (< 0.0)
                0.3,
            ],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to negative values
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes correctly."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs using proper Philadelphia coordinates
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351243200", "212525650"],  # Duplicate OPA ID
            "tree_canopy_gap": [0.1, 0.2, 0.3],
            "geometry": [
                Point(
                    2695530.9812315595, 234150.64579590267
                ),  # Philadelphia coordinates in EPSG:2272
                Point(
                    2695530.9812315595, 234150.64579590267
                ),  # Same geometry for duplicate
                Point(2718195.202635317, 275457.41980949586),
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs
    assert not result.success
    assert len(result.errors) > 0


def test_tree_canopy_validator_statistical_validation():
    """Test that the validator performs statistical validation on larger datasets."""
    # Create a larger dataset with realistic tree canopy gap values
    import numpy as np

    # Generate realistic tree canopy gap data based on the provided statistics
    np.random.seed(42)  # For reproducible results
    n_samples = 1000

    # Generate data with similar distribution to the provided statistics
    # Mean: 0.1688201897, Std: 0.08536259767
    tree_canopy_gaps = np.random.normal(0.1688201897, 0.08536259767, n_samples)

    # Clip to valid range [0.0, 1.0]
    tree_canopy_gaps = np.clip(tree_canopy_gaps, 0.0, 1.0)

    # Add some null values to test non-null percentage
    null_indices = np.random.choice(
        n_samples, size=int(n_samples * 0.0014), replace=False
    )  # 0.14% nulls
    tree_canopy_gaps[null_indices] = np.nan

    # Create proper Philadelphia coordinates in EPSG:2272
    # Philadelphia bounds: (2660574.407687585, 204816.77392398464, 2750112.206304629, 304945.3647740225)
    x_coords = np.random.uniform(2660574, 2750112, n_samples)
    y_coords = np.random.uniform(204816, 304945, n_samples)

    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i:06d}" for i in range(n_samples)],
            "tree_canopy_gap": tree_canopy_gaps,
            "geometry": [Point(x, y) for x, y in zip(x_coords, y_coords)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = TreeCanopyOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass validation with realistic data
    assert result.success
    assert len(result.errors) == 0
