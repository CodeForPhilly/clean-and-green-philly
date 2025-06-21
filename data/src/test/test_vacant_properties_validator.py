import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.vacant_properties import VacantPropertiesOutputValidator


def test_vacant_validator_schema_edge_cases():
    """Test that the vacant properties validator catches schema-level edge cases."""

    # Create synthetic data with schema violations
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650"],
            "vacant": [True, False, "maybe"],  # Invalid: non-boolean value
            "parcel_type": ["Building", "Land", "Invalid"],  # Invalid parcel type
            "market_value": [144800, 158800, -1000],  # Invalid: negative value
            "sale_price": [37000.0, 79900.0, -500.0],  # Invalid: negative value
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-05-23 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2026-01-01 00:00:00+0000", tz="UTC"),  # Future date
            ],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "standardized_street_address": [
                "936 carver st",
                "882 marcella st",
                "9120 ayrdale crescent",
            ],
            "standardized_mailing_address": [
                "5956 harbison ave, philadelphia pa, 19135",
                "882 marcella st, philadelphia pa, 19124-1733",
                "9120 ayrdalecrescent st, philadelphia pa, 19128-1027",
            ],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA"],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
            ],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks disabled
    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-boolean vacant values (schema check)
    assert any("vacant" in msg.lower() for msg in error_messages)

    # Should catch invalid parcel type (schema check)
    assert any("parcel_type" in msg.lower() for msg in error_messages)

    # Should catch negative market value (schema check)
    assert any("market_value" in msg.lower() for msg in error_messages)

    # Should catch negative sale price (schema check)
    assert any("sale_price" in msg.lower() for msg in error_messages)


def test_vacant_validator_schema_valid_data():
    """Test that the vacant properties validator passes with valid schema data."""

    # Create valid synthetic data
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650"],
            "vacant": [True, False, True],  # Valid boolean values
            "parcel_type": ["Building", "Land", "Building"],  # Valid parcel types
            "market_value": [144800, 158800, 382000],
            "sale_price": [37000.0, 79900.0, 1.0],
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-05-23 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-06-01 00:00:00+0000", tz="UTC"),
            ],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "standardized_street_address": [
                "936 carver st",
                "882 marcella st",
                "9120 ayrdale crescent",
            ],
            "standardized_mailing_address": [
                "5956 harbison ave, philadelphia pa, 19135",
                "882 marcella st, philadelphia pa, 19124-1733",
                "9120 ayrdalecrescent st, philadelphia pa, 19128-1027",
            ],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA"],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
            ],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks disabled
    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_vacant_validator_row_level_validation():
    """Test row-level validation logic specifically."""

    # Create data with various edge cases to test row-level validation
    test_data = pd.DataFrame(
        {
            "opa_id": [
                "351243200",
                "351121400",
                "212525650",
                "351243200",
            ],  # Duplicate OPA ID
            "vacant": [True, False, None, True],  # Null value in vacant column
            "parcel_type": [
                "Building",
                "Land",
                "Building",
                "Invalid",
            ],  # Invalid parcel type
            "market_value": [144800, 158800, 382000, 500000],
            "sale_price": [37000.0, 79900.0, 1.0, 100000.0],
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-05-23 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-06-01 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-07-01 00:00:00+0000", tz="UTC"),
            ],
            "zip_code": ["19124", "19124", "19128", "19130"],
            "zoning": ["RSA5", "RSA5", "RMX1", "RSA3"],
            "standardized_street_address": [
                "936 carver st",
                "882 marcella st",
                "9120 ayrdale crescent",
                "1234 test st",
            ],
            "standardized_mailing_address": [
                "5956 harbison ave, philadelphia pa, 19135",
                "882 marcella st, philadelphia pa, 19124-1733",
                "9120 ayrdalecrescent st, philadelphia pa, 19128-1027",
                "1234 test st, philadelphia pa, 19130",
            ],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
                "TEST OWNER",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA", None],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
            ],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
                Point(-75.150, 40.050),
            ],
        }
    )

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = VacantPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]

    # Should catch null values in vacant column
    assert any("null" in msg and "vacant" in msg for msg in error_messages)

    # Should catch duplicate OPA IDs
    assert any("duplicate" in msg and "opa_id" in msg for msg in error_messages)

    # Should catch invalid parcel type
    assert any("invalid" in msg and "parcel_type" in msg for msg in error_messages)


def test_vacant_validator_missing_required_columns():
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

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = VacantPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing required columns
    assert len(errors) > 0
    assert any("missing required columns" in error.lower() for error in errors)

    # Should specifically mention the missing columns
    error_messages = [error.lower() for error in errors]
    assert any("vacant" in msg for msg in error_messages)
    assert any("opa_id" in msg for msg in error_messages)
    assert any("parcel_type" in msg for msg in error_messages)


def test_vacant_validator_non_string_opa_id():
    """Test that the validator catches non-string OPA IDs."""

    # Create data with non-string OPA IDs
    test_data = pd.DataFrame(
        {
            "opa_id": [351243200, 351121400, 212525650],  # Integers instead of strings
            "vacant": [True, False, True],
            "parcel_type": ["Building", "Land", "Building"],
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

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = VacantPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string OPA IDs
    assert len(errors) > 0
    assert any(
        "non-string" in error.lower() and "opa_id" in error.lower() for error in errors
    )


def test_vacant_validator_empty_dataframe():
    """Test that the validator handles empty dataframes gracefully."""

    # Create empty dataframe with required columns
    test_data = pd.DataFrame(
        columns=[
            "opa_id",
            "vacant",
            "parcel_type",
            "market_value",
            "sale_price",
            "zip_code",
            "zoning",
            "geometry",
        ]
    )

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks disabled
    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should handle empty dataframe without crashing
    # May or may not pass depending on schema requirements
    assert isinstance(result.success, bool)
    assert isinstance(result.errors, list)
