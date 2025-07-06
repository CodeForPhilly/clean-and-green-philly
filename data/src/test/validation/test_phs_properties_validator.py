import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.phs_properties import PHSPropertiesOutputValidator


def _create_phs_test_data(base_test_data):
    """Create test data with only the columns expected by the PHS properties validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "phs_care_program": ["Community LandCare", "Philadelphia LandCare", None],
            "geometry": base_test_data["geometry"],
        }
    )


def test_phs_validator_schema_valid_data(base_test_data):
    """Test that the PHS validator passes with valid schema data."""
    # Create valid test data
    test_data = _create_phs_test_data(base_test_data)

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success


def test_phs_validator_schema_edge_cases(base_test_data):
    """Test that the PHS validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = base_test_data.copy()
    test_data["phs_care_program"] = [
        "Community LandCare",
        123,
        None,
    ]  # Non-string value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-string phs_care_program value (schema check)
    assert any("phs_care_program" in msg.lower() for msg in error_messages)


def test_phs_validator_row_level_validation(base_test_data):
    """Test row-level validation logic specifically."""
    # Create data with non-string values to test row-level validation
    test_data = base_test_data.copy()
    test_data["phs_care_program"] = [
        "Community LandCare",
        456,
        "Philadelphia LandCare",
    ]  # Integer value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PHSPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string phs_care_program values
    assert len(errors) > 0
    assert any(
        "non-string" in error.lower() and "phs_care_program" in error.lower()
        for error in errors
    )


def test_phs_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Create data missing required columns
    test_data = pd.DataFrame(
        {
            "phs_care_program": ["Community LandCare", "Philadelphia LandCare", None],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PHSPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing required columns
    assert len(errors) > 0
    assert any("missing required columns" in error.lower() for error in errors)

    # Should specifically mention the missing opa_id column
    error_messages = [error.lower() for error in errors]
    assert any("opa_id" in msg for msg in error_messages)


def test_phs_validator_null_values(base_test_data):
    """Test that the validator handles null values correctly."""
    test_data = base_test_data.copy()
    test_data["phs_care_program"] = [
        "Community LandCare",
        None,
        "Philadelphia LandCare",
    ]  # Null value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with null values (they are allowed in schema)
    assert result.success
    assert len(result.errors) == 0


def test_phs_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(columns=["opa_id", "phs_care_program", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_phs_validator_missing_phs_care_program_column(base_test_data):
    """Test that the validator catches missing phs_care_program column correctly."""
    # Test with missing phs_care_program column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing phs_care_program column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail since phs_care_program is required
    assert not result.success
    assert len(result.errors) > 0

    print("PHS VALIDATOR ERRORS:", result.errors)

    # Check that it caught the missing column
    error_messages = [str(error) for error in result.errors]
    assert any("schema validation failed" in msg.lower() for msg in error_messages)
    assert any("phs_care_program" in msg.lower() for msg in error_messages)


def test_phs_validator_statistical_validation(base_test_data):
    """Test statistical validation with larger dataset."""
    n = 200
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set 5% to a real program, rest to None
    test_data["phs_care_program"] = [
        "Community LandCare" if i < 10 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass with reasonable PHS coverage
    assert result.success
    assert len(result.errors) == 0


def test_phs_validator_statistical_validation_high_coverage(base_test_data):
    """Test statistical validation with unreasonably high PHS coverage."""
    n = 200
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set 50% to a real program, rest to None
    test_data["phs_care_program"] = [
        "Community LandCare" if i < 100 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to unreasonably high PHS coverage
    assert not result.success
    assert len(result.errors) > 0
    assert any(
        "phs care program percentage" in str(error).lower() for error in result.errors
    )


def test_phs_validator_statistical_validation_low_coverage(base_test_data):
    """Test statistical validation with unreasonably low PHS coverage."""
    n = 200
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set 0.5% to a real program, rest to None
    test_data["phs_care_program"] = [
        "Community LandCare" if i < 1 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to unreasonably low PHS coverage
    assert not result.success
    assert len(result.errors) > 0
    assert any(
        "phs care program percentage" in str(error).lower() for error in result.errors
    )


def test_phs_validator_mixed_data_types(base_test_data):
    """Test that the validator catches mixed data types in phs_care_program."""
    test_data = base_test_data.copy()
    # Fix the length to match the base_test_data length
    test_data["phs_care_program"] = [
        "Community LandCare",
        123.45,  # Float
        True,  # Boolean
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PHSPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string values
    assert not result.success
    assert len(result.errors) > 0

    # Check that it caught the non-string values
    error_messages = [str(error) for error in result.errors]
    assert any(
        "non-string" in msg.lower() and "phs_care_program" in msg.lower()
        for msg in error_messages
    )
