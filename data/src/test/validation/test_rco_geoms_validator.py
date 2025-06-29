import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.rco_geoms import RCOGeomsOutputValidator


def _create_rco_test_data(base_test_data):
    """Create test data with only the columns expected by the RCO validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "rco_info": ["RCO Info 1", "RCO Info 2", "RCO Info 3"],
            "rco_names": ["RCO Name 1", "RCO Name 2", "RCO Name 3"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_rco_geoms_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_rco_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_rco_geoms_validator_schema_edge_cases(base_test_data):
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "rco_info": ["RCO Info 1", "RCO Info 2", "RCO Info 3"],
            # Missing rco_names column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing rco_names column
    assert not result.success
    assert len(result.errors) > 0

    # Test with null rco_info values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "rco_info": ["RCO Info 1", None, "RCO Info 3"],  # Null value
            "rco_names": ["RCO Name 1", "RCO Name 2", "RCO Name 3"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null rco_info values
    assert not result.success
    assert len(result.errors) > 0


def test_rco_geoms_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_rco_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_rco_geoms_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "rco_info": ["RCO Info 1", "RCO Info 2", "RCO Info 3"],
            "rco_names": ["RCO Name 1", "RCO Name 2", "RCO Name 3"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0


def test_rco_geoms_validator_non_string_rco_info(base_test_data):
    """Test that the validator catches non-string rco_info values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "rco_info": ["RCO Info 1", 123, "RCO Info 3"],  # Non-string value
            "rco_names": ["RCO Name 1", "RCO Name 2", "RCO Name 3"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string rco_info values
    assert not result.success
    assert len(result.errors) > 0


def test_rco_geoms_validator_non_string_rco_names(base_test_data):
    """Test that the validator catches non-string rco_names values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "rco_info": ["RCO Info 1", "RCO Info 2", "RCO Info 3"],
            "rco_names": ["RCO Name 1", 456, "RCO Name 3"],  # Non-string value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string rco_names values
    assert not result.success
    assert len(result.errors) > 0


def test_rco_geoms_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes correctly."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_rco_geoms_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    test_data = _create_rco_test_data(base_test_data)

    # Add a duplicate OPA ID
    duplicate_row = test_data.iloc[0].copy()
    duplicate_row["opa_id"] = "351243200"  # Duplicate
    test_data = pd.concat([test_data, pd.DataFrame([duplicate_row])], ignore_index=True)

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = RCOGeomsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs
    assert not result.success
    assert len(result.errors) > 0
