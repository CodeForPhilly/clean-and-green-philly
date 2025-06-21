import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from src.config.config import USE_CRS
from src.validation.pwd_parcels import PWDParcelsOutputValidator


def test_pwd_validator_schema_edge_cases(base_test_data):
    """Test that the PWD parcels validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = base_test_data.copy()
    test_data["is_condo_unit"] = [True, False, "maybe"]  # Invalid: non-boolean value
    test_data["parcel_area_sqft"] = [1000.0, 2000.0, -100.0]  # Invalid: negative area
    test_data.loc[2, "market_value"] = -1000  # Invalid: negative value
    test_data.loc[2, "sale_price"] = -500.0  # Invalid: negative value
    test_data.loc[2, "sale_date"] = pd.Timestamp(
        "2026-01-01 00:00:00+0000", tz="UTC"
    )  # Future date

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PWDParcelsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-boolean is_condo_unit values (schema check)
    assert any("is_condo_unit" in msg.lower() for msg in error_messages)

    # Should catch negative parcel area (schema check)
    assert any("parcel_area_sqft" in msg.lower() for msg in error_messages)

    # Should catch negative market value (schema check)
    assert any("market_value" in msg.lower() for msg in error_messages)

    # Should catch negative sale price (schema check)
    assert any("sale_price" in msg.lower() for msg in error_messages)


def test_pwd_validator_schema_valid_data(base_test_data):
    """Test that the PWD parcels validator passes with valid schema data."""
    # Create valid test data
    test_data = base_test_data.copy()
    test_data["is_condo_unit"] = [True, False, True]  # Valid boolean values
    test_data["parcel_area_sqft"] = [
        0.0,
        2000.0,
        0.0,
    ]  # Valid areas (0.0 for condo units)

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PWDParcelsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_pwd_validator_row_level_validation(base_test_data):
    """Test row-level validation logic specifically."""
    # Create data with various edge cases
    test_data = base_test_data.copy()
    test_data["is_condo_unit"] = [
        True,
        False,
        None,
    ]  # Null value in is_condo_unit column
    test_data["parcel_area_sqft"] = [0.0, 2000.0, 3000.0]

    # Add a duplicate OPA ID
    duplicate_row = test_data.iloc[0].copy()
    duplicate_row["opa_id"] = "351243200"  # Duplicate
    test_data = pd.concat([test_data, pd.DataFrame([duplicate_row])], ignore_index=True)

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PWDParcelsOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]

    # Should catch null values in is_condo_unit column
    assert any("null" in msg and "is_condo_unit" in msg for msg in error_messages)

    # Should catch duplicate OPA IDs
    assert any("duplicate" in msg and "opa_id" in msg for msg in error_messages)


def test_pwd_validator_missing_required_columns():
    """Test that the validator catches missing required columns."""
    # Create data missing required columns
    test_data = pd.DataFrame(
        {
            "market_value": [144800, 158800, 382000],
            "sale_price": [37000.0, 79900.0, 1.0],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PWDParcelsOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing required columns
    assert len(errors) > 0
    assert any("missing required columns" in error.lower() for error in errors)

    # Should specifically mention the missing columns
    error_messages = [error.lower() for error in errors]
    assert any("is_condo_unit" in msg for msg in error_messages)
    assert any("opa_id" in msg for msg in error_messages)
    assert any("parcel_area_sqft" in msg for msg in error_messages)


def test_pwd_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA IDs."""
    # Create data with non-string OPA IDs
    test_data = base_test_data.copy()
    test_data["is_condo_unit"] = [True, False, True]
    test_data["parcel_area_sqft"] = [0.0, 2000.0, 0.0]
    test_data["opa_id"] = [
        351243200,
        351121400,
        212525650,
    ]  # Integers instead of strings

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PWDParcelsOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string OPA IDs
    assert len(errors) > 0
    assert any(
        "non-string" in error.lower() and "opa_id" in error.lower() for error in errors
    )


def test_pwd_validator_geometry_type_consistency():
    """Test that the validator catches geometry type inconsistencies."""
    # Create data with condo units that have polygon geometries (should be points)
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650"],
            "is_condo_unit": [True, True, False],  # First two are condo units
            "parcel_area_sqft": [0.0, 0.0, 2000.0],
            "geometry": [
                Polygon(
                    [
                        (-75.089, 40.033),
                        (-75.088, 40.033),
                        (-75.088, 40.034),
                        (-75.089, 40.034),
                    ]
                ),  # Condo with polygon (invalid)
                Point(-75.093, 40.031),  # Condo with point (valid)
                Point(-75.244, 40.072),  # Non-condo with point (valid)
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly (since this is a statistical check)
    validator = PWDParcelsOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch condo units with non-point geometries
    assert len(errors) > 0
    assert any("non-point geometries" in error.lower() for error in errors)


def test_pwd_validator_condo_area_validation():
    """Test that the validator catches condo units with non-zero areas."""
    # Create data with condo units that have non-zero areas (should be 0.0)
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650"],
            "is_condo_unit": [True, True, False],
            "parcel_area_sqft": [
                100.0,
                0.0,
                2000.0,
            ],  # First condo has non-zero area (invalid)
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = PWDParcelsOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch condo units with non-zero areas
    assert len(errors) > 0
    assert any("non-zero parcel area" in error.lower() for error in errors)


def test_pwd_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes gracefully."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks disabled
    validator = PWDParcelsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should handle empty dataframe without crashing
    # May or may not pass depending on schema requirements
    assert isinstance(result.success, bool)
    assert isinstance(result.errors, list)


def test_pwd_validator_small_dataset_statistical_checks(base_test_data):
    """Test that statistical checks are skipped for small datasets."""
    # Create small dataset (less than 100 rows)
    test_data = base_test_data.copy()
    test_data["is_condo_unit"] = [True, False, True]
    test_data["parcel_area_sqft"] = [0.0, 2000.0, 0.0]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks enabled
    validator = PWDParcelsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass because statistical checks are skipped for small datasets
    assert result.success
