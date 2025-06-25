import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.vacant_properties import VacantPropertiesOutputValidator


def test_vacant_validator_schema_edge_cases(base_test_data):
    """Test that the vacant properties validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = base_test_data.copy()
    test_data["vacant"] = [True, False, "maybe"]  # Invalid: non-boolean value
    test_data["parcel_type"] = ["Building", "Land", "Invalid"]  # Invalid parcel type

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    print("VACANT VALIDATOR ERRORS:", result.errors)

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch invalid parcel type (schema check)
    assert any("parcel_type" in msg.lower() for msg in error_messages)

    # Test row-level validation directly to catch non-boolean values in vacant column
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-boolean values in vacant column (row-level check)
    assert any(
        "non-boolean" in msg.lower() and "vacant" in msg.lower() for msg in errors
    )


def test_vacant_validator_schema_valid_data(base_test_data):
    """Test that the vacant properties validator passes with valid schema data."""
    # Create valid test data
    test_data = base_test_data.copy()
    test_data["vacant"] = [True, False, True]  # Valid boolean values
    test_data["parcel_type"] = ["Building", "Land", "Building"]  # Valid parcel types

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_vacant_validator_row_level_validation(base_test_data):
    """Test row-level validation logic specifically."""
    # Create data with various edge cases to test row-level validation
    test_data = base_test_data.copy()
    test_data["vacant"] = [True, False, None]  # Null value in vacant column
    test_data["parcel_type"] = ["Building", "Land", "Invalid"]  # Invalid parcel type

    # Add a duplicate OPA ID
    duplicate_row = test_data.iloc[0].copy()
    duplicate_row["opa_id"] = "351243200"  # Duplicate
    test_data = pd.concat([test_data, pd.DataFrame([duplicate_row])], ignore_index=True)

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

    # Should catch invalid parcel types
    assert any(
        "invalid values in 'parcel_type' column" in msg for msg in error_messages
    )


def test_vacant_validator_missing_required_columns():
    """Test that the validator catches missing required columns."""
    # Create data missing required columns
    test_data = pd.DataFrame(
        {
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )

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


def test_vacant_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA IDs."""
    # Create data with non-string OPA IDs
    test_data = base_test_data.copy()
    test_data["vacant"] = [True, False, True]
    test_data["parcel_type"] = ["Building", "Land", "Building"]
    test_data["opa_id"] = [
        351243200,
        351121400,
        212525650,
    ]  # Integers instead of strings

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


def test_vacant_validator_empty_dataframe(empty_dataframe):
    """Test that the validator handles empty dataframes gracefully."""
    gdf = gpd.GeoDataFrame(empty_dataframe, geometry="geometry", crs=USE_CRS)

    # Test validator with statistical checks disabled
    validator = VacantPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should handle empty dataframe without crashing
    # May or may not pass depending on schema requirements
    assert isinstance(result.success, bool)
    assert isinstance(result.errors, list)
