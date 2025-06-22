import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.city_owned_properties import CityOwnedPropertiesOutputValidator


def _create_city_owned_test_data(base_test_data):
    """Create test data with only the columns expected by the city owned properties validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "city_owner_agency": ["Land Bank (PHDC)", "PHA", "City of Philadelphia"],
            "side_yard_eligible": [True, False, True],
            "geometry": base_test_data["geometry"],
        }
    )


def test_city_owned_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_city_owned_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_city_owned_validator_schema_edge_cases(base_test_data):
    """Test that the validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = _create_city_owned_test_data(base_test_data)
    test_data.loc[1, "city_owner_agency"] = 123  # Non-string value
    test_data.loc[2, "side_yard_eligible"] = "maybe"  # Non-boolean value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-string city_owner_agency (schema check)
    assert any("city_owner_agency" in msg.lower() for msg in error_messages)

    # Should catch non-boolean side_yard_eligible (schema check)
    assert any("side_yard_eligible" in msg.lower() for msg in error_messages)


def test_city_owned_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_city_owned_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_city_owned_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing city_owner_agency column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing city_owner_agency column
            "side_yard_eligible": [True, False, True],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing city_owner_agency column
    assert not result.success
    assert len(result.errors) > 0


def test_city_owned_validator_non_string_city_owner_agency(base_test_data):
    """Test that the validator catches non-string city_owner_agency values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "city_owner_agency": [
                "Land Bank (PHDC)",
                123,
                "City of Philadelphia",
            ],  # Non-string value
            "side_yard_eligible": [True, False, True],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string city_owner_agency values
    assert not result.success
    assert len(result.errors) > 0


def test_city_owned_validator_non_boolean_side_yard_eligible(base_test_data):
    """Test that the validator catches non-boolean side_yard_eligible values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "city_owner_agency": ["Land Bank (PHDC)", "PHA", "City of Philadelphia"],
            "side_yard_eligible": [True, "maybe", True],  # Non-boolean value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-boolean side_yard_eligible values
    assert not result.success
    assert len(result.errors) > 0


def test_city_owned_validator_null_values(base_test_data):
    """Test that the validator handles null values correctly."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "city_owner_agency": [
                "Land Bank (PHDC)",
                None,
                "City of Philadelphia",
            ],  # Null value
            "side_yard_eligible": [True, False, None],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with null values (they are allowed in schema)
    assert result.success
    assert len(result.errors) == 0


def test_city_owned_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(
        columns=["opa_id", "city_owner_agency", "side_yard_eligible", "geometry"]
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_city_owned_validator_row_level_validation_direct(base_test_data):
    """Test row-level validation logic directly."""
    # Create data with various edge cases to test row-level validation
    test_data = _create_city_owned_test_data(base_test_data)
    test_data.loc[1, "city_owner_agency"] = 456  # Non-string value
    test_data.loc[2, "side_yard_eligible"] = "yes"  # Non-boolean value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CityOwnedPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]

    # Should catch non-string city_owner_agency values
    assert any(
        "non-string" in msg and "city_owner_agency" in msg for msg in error_messages
    )

    # Should catch non-boolean side_yard_eligible values
    assert any(
        "non-boolean" in msg and "side_yard_eligible" in msg for msg in error_messages
    )


def test_city_owned_validator_missing_side_yard_eligible_column(base_test_data):
    """Test that the validator catches missing side_yard_eligible column."""
    # Test with missing side_yard_eligible column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "city_owner_agency": ["Land Bank (PHDC)", "PHA", "City of Philadelphia"],
            # Missing side_yard_eligible column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CityOwnedPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing side_yard_eligible column
    assert not result.success
    assert len(result.errors) > 0
