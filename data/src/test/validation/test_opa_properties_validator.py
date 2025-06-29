import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.opa_properties import OPAPropertiesOutputValidator


def test_opa_validator_schema_edge_cases(base_test_data):
    """Test that the OPA validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = base_test_data.copy()
    test_data["parcel_type"] = [
        "Building",
        "Building",
        "Invalid",
    ]  # Invalid parcel type
    test_data["street_address"] = [
        "936 CARVER ST",
        "882 MARCELLA ST",
        "9120 AYRDALE CRESCENT",
    ]
    test_data.loc[2, "market_value"] = -1000  # Negative market value
    test_data.loc[2, "sale_price"] = -500.0  # Negative sale price
    test_data.loc[2, "sale_date"] = pd.Timestamp(
        "2026-01-01 00:00:00+0000", tz="UTC"
    )  # Future date

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OPAPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch invalid parcel type (schema check)
    assert any("parcel_type" in msg.lower() for msg in error_messages)

    # Should catch negative market value (schema check)
    assert any("market_value" in msg.lower() for msg in error_messages)

    # Should catch negative sale price (schema check)
    assert any("sale_price" in msg.lower() for msg in error_messages)


def test_opa_validator_schema_valid_data(base_test_data):
    """Test that the OPA validator passes with valid schema data."""
    # Create valid test data
    test_data = base_test_data.copy()
    test_data["parcel_type"] = ["Building", "Building", "Building"]
    test_data["street_address"] = [
        "936 CARVER ST",
        "882 MARCELLA ST",
        "9120 AYRDALE CRESCENT",
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OPAPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_opa_validator_row_level_validation(base_test_data):
    """Test row-level validation logic specifically."""
    # Create data with future dates to test row-level validation
    test_data = base_test_data.copy()
    test_data["parcel_type"] = ["Building", "Building", "Building"]
    test_data["street_address"] = [
        "936 CARVER ST",
        "882 MARCELLA ST",
        "9120 AYRDALE CRESCENT",
    ]
    test_data.loc[1, "sale_date"] = pd.Timestamp(
        "2026-01-01 00:00:00+0000", tz="UTC"
    )  # Future date

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = OPAPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch future sale date
    assert len(errors) > 0
    assert any("future" in error.lower() for error in errors)
