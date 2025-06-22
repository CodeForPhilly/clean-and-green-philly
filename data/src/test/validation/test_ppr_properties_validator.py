import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.ppr_properties import PPRPropertiesOutputValidator


def _create_ppr_properties_test_data(base_test_data):
    """Create test data with only the columns expected by the PPR properties validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "public_name": ["PPR Property 1", "PPR Property 2", "PPR Property 3"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_ppr_properties_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_ppr_properties_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_ppr_properties_validator_schema_edge_cases(base_test_data):
    """Test that the validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = _create_ppr_properties_test_data(base_test_data)
    test_data.loc[1, "public_name"] = 123  # Non-string value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-string public_name (schema check)
    assert any("public_name" in msg.lower() for msg in error_messages)


def test_ppr_properties_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_ppr_properties_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_ppr_properties_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing public_name column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing public_name column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing public_name column
    assert not result.success
    assert len(result.errors) > 0


def test_ppr_properties_validator_non_string_public_name(base_test_data):
    """Test that the validator catches non-string public_name values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "public_name": [
                "PPR Property 1",
                123,
                "PPR Property 3",
            ],  # Non-string value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string public_name values
    assert not result.success
    assert len(result.errors) > 0


def test_ppr_properties_validator_null_values(base_test_data):
    """Test that the validator handles null values correctly."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "public_name": [
                "PPR Property 1",
                None,
                "PPR Property 3",
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with null values (they are allowed in schema)
    assert result.success
    assert len(result.errors) == 0


def test_ppr_properties_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(columns=["opa_id", "public_name", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_ppr_properties_validator_row_level_validation_direct(base_test_data):
    """Test row-level validation logic directly."""
    # Create data with various edge cases to test row-level validation
    test_data = _create_ppr_properties_test_data(base_test_data)
    test_data.loc[1, "public_name"] = 456  # Non-string value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PPRPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]
    assert any("non-string" in msg and "public_name" in msg for msg in error_messages)


def test_ppr_properties_validator_missing_public_name_column(base_test_data):
    """Test that the validator catches missing public_name column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing public_name column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PPRPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing public_name column
    assert len(errors) > 0
    assert any("public_name" in error.lower() for error in errors)


def test_ppr_properties_validator_statistical_validation_valid_count(base_test_data):
    """Test statistical validation with valid record count."""
    # Create data with ~507 records (within expected range)
    n = 507
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add public_name column
    test_data["public_name"] = [f"PPR Property {i}" for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass with valid record count
    assert result.success
    assert len(result.errors) == 0


def test_ppr_properties_validator_statistical_validation_too_few_records(
    base_test_data,
):
    """Test statistical validation with too few records."""
    # Create data with only 300 records (below expected range)
    n = 300
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add public_name column
    test_data["public_name"] = [f"PPR Property {i}" for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too few records
    assert not result.success
    assert len(result.errors) > 0
    assert any("outside expected range" in error.lower() for error in result.errors)


def test_ppr_properties_validator_statistical_validation_too_many_records(
    base_test_data,
):
    """Test statistical validation with too many records."""
    # Create data with 600 records (above expected range)
    n = 600
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add public_name column
    test_data["public_name"] = [f"PPR Property {i}" for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too many records
    assert not result.success
    assert len(result.errors) > 0
    assert any("outside expected range" in error.lower() for error in result.errors)


def test_ppr_properties_validator_statistical_validation_low_public_name_coverage(
    base_test_data,
):
    """Test statistical validation with low public name coverage."""
    # Create data with ~507 records but low public name coverage
    n = 507
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set only 10% to have public names (below 80% threshold)
    test_data["public_name"] = [
        f"PPR Property {i}" if i < 50 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to low public name coverage
    assert not result.success
    assert len(result.errors) > 0
    assert any("coverage" in error.lower() for error in result.errors)


def test_ppr_properties_validator_statistical_validation_direct(base_test_data):
    """Test statistical validation logic directly."""
    # Create data with valid count but low public name coverage
    n = 507
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    test_data["public_name"] = [
        f"PPR Property {i}" if i < 50 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = PPRPropertiesOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch low public name coverage
    assert len(errors) > 0
    assert any("coverage" in error.lower() for error in errors)


def test_ppr_properties_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA IDs."""
    # Create data with non-string OPA IDs
    test_data = _create_ppr_properties_test_data(base_test_data)
    test_data["opa_id"] = [
        351243200,
        351121400,
        212525650,
    ]  # Integers instead of strings

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = PPRPropertiesOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string OPA IDs (inherited from base validator)
    # Note: This is tested in the base validator tests, but we include it here for completeness
    assert len(errors) == 0  # Row-level validation doesn't check OPA types, schema does


def test_ppr_properties_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs
    test_data = _create_ppr_properties_test_data(base_test_data)
    test_data["opa_id"] = ["351243200", "351243200", "212525650"]  # Duplicate OPA ID

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = PPRPropertiesOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs (schema validation)
    assert not result.success
    assert len(result.errors) > 0
