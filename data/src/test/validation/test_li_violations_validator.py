import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.li_violations import LIViolationsOutputValidator


def _create_li_violations_test_data(base_test_data):
    """Create test data with only the columns expected by the LI violations validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, 1, 2],  # Valid integer values
            "open_violations_past_year": [0, 0, 1],  # Valid integer values
            "geometry": base_test_data["geometry"],
        }
    )


def test_li_violations_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_li_violations_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_li_violations_validator_schema_edge_cases(base_test_data):
    """Test that the validator handles edge cases correctly."""
    # Test with missing required columns
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing all_violations_past_year and open_violations_past_year columns
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing violation columns
    assert not result.success
    assert len(result.errors) > 0

    # Test with null violation values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, None, 2],  # Null value
            "open_violations_past_year": [0, 0, None],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null violation values
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_li_violations_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_li_violations_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing opa_id column
    test_data = pd.DataFrame(
        {
            # Missing opa_id column
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing opa_id column
    assert not result.success
    assert len(result.errors) > 0

    # Test with missing all_violations_past_year column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing all_violations_past_year column
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing all_violations_past_year column
    assert not result.success
    assert len(result.errors) > 0

    # Test with missing open_violations_past_year column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, 1, 2],
            # Missing open_violations_past_year column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing open_violations_past_year column
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_non_integer_all_violations(base_test_data):
    """Test that the validator catches non-integer all_violations_past_year values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [
                0,
                "maybe",
                2,
            ],  # Non-integer value
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-integer all_violations_past_year values
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_non_integer_open_violations(base_test_data):
    """Test that the validator catches non-integer open_violations_past_year values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [
                0,
                0.5,
                1,
            ],  # Non-integer value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-integer open_violations_past_year values
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_null_all_violations_values(base_test_data):
    """Test that the validator catches null values in all_violations_past_year column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [
                0,
                None,
                2,
            ],  # Null value
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null values in all_violations_past_year column
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_null_open_violations_values(base_test_data):
    """Test that the validator catches null values in open_violations_past_year column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [
                0,
                None,
                1,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null values in open_violations_past_year column
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_negative_values(base_test_data):
    """Test that the validator catches negative values in violation columns."""
    # Test with negative all_violations_past_year values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [
                0,
                -1,
                2,
            ],  # Negative value
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to negative all_violations_past_year values
    assert not result.success
    assert len(result.errors) > 0

    # Test with negative open_violations_past_year values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [
                0,
                -1,
                1,
            ],  # Negative value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to negative open_violations_past_year values
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes correctly."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing required columns in empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs using proper Philadelphia coordinates
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351243200", "212525650"],  # Duplicate OPA ID
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [0, 0, 1],
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

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA ID values."""
    test_data = pd.DataFrame(
        {
            "opa_id": [
                "351243200",
                123456789,  # Non-string OPA ID
                "212525650",
            ],
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string OPA ID values
    assert not result.success
    assert len(result.errors) > 0


def test_li_violations_validator_null_opa_id(base_test_data):
    """Test that the validator catches null OPA ID values."""
    test_data = pd.DataFrame(
        {
            "opa_id": [
                "351243200",
                None,  # Null OPA ID
                "212525650",
            ],
            "all_violations_past_year": [0, 1, 2],
            "open_violations_past_year": [0, 0, 1],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = LIViolationsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null OPA ID values
    assert not result.success
    assert len(result.errors) > 0
