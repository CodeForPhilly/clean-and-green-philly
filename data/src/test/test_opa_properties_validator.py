import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.opa_properties import OPAPropertiesOutputValidator


def test_opa_validator_schema_edge_cases():
    """Test that the OPA validator catches schema-level edge cases."""

    # Create synthetic data with schema violations
    test_data = pd.DataFrame(
        {
            "market_value": [
                144800,
                -1,
                999999999,
            ],  # Valid, negative (invalid), extreme
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                None,  # Missing date (valid)
                pd.Timestamp(
                    "2026-01-01 00:00:00+0000", tz="UTC"
                ),  # Future date (invalid)
            ],
            "sale_price": [37000.0, 0.0, -1000.0],  # Valid, zero, negative (invalid)
            "opa_id": ["351243200", "351121400", "212525650"],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA"],
            "street_address": [
                "936 CARVER ST",
                "882 MARCELLA ST",
                "9120 AYRDALE CRESCENT",
            ],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
            ],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "parcel_type": ["Building", "Land", "Invalid"],  # Invalid parcel type
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
    validator = OPAPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch negative market value (schema check)
    assert any("market_value" in msg.lower() for msg in error_messages)

    # Should catch future sale date (row-level check)
    assert any("future" in msg.lower() for msg in error_messages)

    # Should catch invalid parcel type (schema check)
    assert any("parcel_type" in msg.lower() for msg in error_messages)


def test_opa_validator_schema_valid_data():
    """Test that the OPA validator passes with valid schema data."""

    # Create valid synthetic data using exact sample values
    test_data = pd.DataFrame(
        {
            "market_value": [144800, 158800, 382000],
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-05-23 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-06-01 00:00:00+0000", tz="UTC"),
            ],
            "sale_price": [37000.0, 79900.0, 1.0],
            "opa_id": ["351243200", "351121400", "212525650"],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA"],
            "street_address": [
                "936 CARVER ST",
                "882 MARCELLA ST",
                "9120 AYRDALE CRESCENT",
            ],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
            ],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "parcel_type": ["Building", "Building", "Building"],
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
    validator = OPAPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_opa_validator_row_level_validation():
    """Test row-level validation logic specifically."""

    # Create data with future dates to test row-level validation
    test_data = pd.DataFrame(
        {
            "market_value": [144800, 158800],
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp(
                    "2026-01-01 00:00:00+0000", tz="UTC"
                ),  # Future date (next year)
            ],
            "sale_price": [37000.0, 79900.0],
            "opa_id": ["351243200", "351121400"],
            "owner_1": ["SKYLUCK HORIZON REALTY IN", "PRESLEY MARY"],
            "owner_2": [None, None],
            "street_address": ["936 CARVER ST", "882 MARCELLA ST"],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
            ],
            "zip_code": ["19124", "19124"],
            "zoning": ["RSA5", "RSA5"],
            "parcel_type": ["Building", "Building"],
            "standardized_street_address": ["936 carver st", "882 marcella st"],
            "standardized_mailing_address": [
                "5956 harbison ave, philadelphia pa, 19135",
                "882 marcella st, philadelphia pa, 19124-1733",
            ],
            "geometry": [Point(-75.089, 40.033), Point(-75.093, 40.031)],
        }
    )

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = OPAPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch future sale date
    assert len(errors) > 0
    assert any("future" in error.lower() for error in errors)
