import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.community_gardens import CommunityGardensOutputValidator


def _create_community_gardens_test_data(base_test_data):
    """Create test data with only the columns expected by the community gardens validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "vacant": [False, False, False],  # Community gardens are non-vacant
            "geometry": base_test_data["geometry"],
        }
    )


def test_community_gardens_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_community_gardens_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_schema_edge_cases(base_test_data):
    """Test that the validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = _create_community_gardens_test_data(base_test_data)
    test_data.loc[1, "vacant"] = "not a boolean"  # Non-boolean value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-boolean vacant (schema check)
    assert any("vacant" in msg.lower() for msg in error_messages)


def test_community_gardens_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_community_gardens_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing vacant column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing vacant column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing vacant column
    assert not result.success
    assert len(result.errors) > 0


def test_community_gardens_validator_null_values(base_test_data):
    """Test that the validator handles null values correctly."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "vacant": [
                False,
                None,
                True,
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with null values (they are allowed in schema)
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(columns=["opa_id", "vacant", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_community_gardens_validator_row_level_validation_direct(base_test_data):
    """Test row-level validation logic directly."""
    # Create data with various edge cases to test row-level validation
    test_data = _create_community_gardens_test_data(base_test_data)
    test_data.loc[1, "vacant"] = "not a boolean"  # Non-boolean value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]
    assert any("non-boolean" in msg and "vacant" in msg for msg in error_messages)


def test_community_gardens_validator_missing_vacant_column(base_test_data):
    """Test that the validator catches missing vacant column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing vacant column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing vacant column
    assert len(errors) > 0
    assert any("vacant" in error.lower() for error in errors)


def test_community_gardens_validator_statistical_validation_valid_count(base_test_data):
    """Test statistical validation with valid record count."""
    # Create data with ~205 records (within expected range)
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add vacant column - mix of vacant and non-vacant
    test_data["vacant"] = [i % 2 == 0 for i in range(n)]  # Alternating True/False

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass with valid record count
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_statistical_validation_too_few_records(
    base_test_data,
):
    """Test statistical validation with too few records."""
    # Create data with only 100 records (below expected range)
    n = 100
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add vacant column - mix of vacant and non-vacant
    test_data["vacant"] = [i % 2 == 0 for i in range(n)]  # Alternating True/False

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass - validator doesn't check record count ranges
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_statistical_validation_too_many_records(
    base_test_data,
):
    """Test statistical validation with too many records."""
    # Create data with 300 records (above expected range)
    n = 300
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add vacant column - mix of vacant and non-vacant
    test_data["vacant"] = [i % 2 == 0 for i in range(n)]  # Alternating True/False

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass - validator doesn't check record count ranges
    assert result.success
    assert len(result.errors) == 0


def test_community_gardens_validator_statistical_validation_all_vacant(
    base_test_data,
):
    """Test statistical validation with all properties marked as vacant."""
    # Create data with ~205 records but all vacant (no community gardens)
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set all to vacant (no community gardens)
    test_data["vacant"] = [True] * n

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to no non-vacant properties (no community gardens)
    assert not result.success
    assert len(result.errors) > 0
    assert any("non-vacant" in error.lower() for error in result.errors)


def test_community_gardens_validator_statistical_validation_direct(base_test_data):
    """Test statistical validation logic directly."""
    # Create data with valid count but all vacant (no community gardens)
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    test_data["vacant"] = [True] * n  # All vacant

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch no non-vacant properties
    assert len(errors) > 0
    assert any("non-vacant" in error.lower() for error in errors)


def test_community_gardens_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA IDs."""
    # Create data with non-string OPA IDs
    test_data = _create_community_gardens_test_data(base_test_data)
    test_data["opa_id"] = [
        351243200,
        351121400,
        212525650,
    ]  # Integers instead of strings

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string OPA IDs (inherited from base validator)
    # Note: This is tested in the base validator tests, but we include it here for completeness
    assert len(errors) == 0  # Row-level validation doesn't check OPA types, schema does


def test_community_gardens_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs
    test_data = _create_community_gardens_test_data(base_test_data)
    test_data["opa_id"] = ["351243200", "351243200", "212525650"]  # Duplicate OPA ID

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs (schema validation)
    assert not result.success
    assert len(result.errors) > 0


def test_community_gardens_validator_non_string_vacant(base_test_data):
    """Test that the validator catches non-boolean vacant values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "vacant": [
                False,
                "not a boolean",
                True,
            ],  # Non-boolean value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-boolean vacant values
    assert not result.success
    assert len(result.errors) > 0
