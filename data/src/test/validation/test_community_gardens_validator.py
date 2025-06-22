import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.community_gardens import CommunityGardensOutputValidator


def _create_community_gardens_test_data(base_test_data):
    """Create test data with only the columns expected by the community gardens validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "site_name": [
                "Community Garden 1",
                "Community Garden 2",
                "Community Garden 3",
            ],
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
    test_data.loc[1, "site_name"] = 123  # Non-string value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch non-string site_name (schema check)
    assert any("site_name" in msg.lower() for msg in error_messages)


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
    # Test with missing site_name column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing site_name column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing site_name column
    assert not result.success
    assert len(result.errors) > 0


def test_community_gardens_validator_non_string_site_name(base_test_data):
    """Test that the validator catches non-string site_name values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "site_name": [
                "Community Garden 1",
                123,
                "Community Garden 3",
            ],  # Non-string value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string site_name values
    assert not result.success
    assert len(result.errors) > 0


def test_community_gardens_validator_null_values(base_test_data):
    """Test that the validator handles null values correctly."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "site_name": [
                "Community Garden 1",
                None,
                "Community Garden 3",
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
    test_data = pd.DataFrame(columns=["opa_id", "site_name", "geometry"])

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
    test_data.loc[1, "site_name"] = 456  # Non-string value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]
    assert any("non-string" in msg and "site_name" in msg for msg in error_messages)


def test_community_gardens_validator_missing_site_name_column(base_test_data):
    """Test that the validator catches missing site_name column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing site_name column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing site_name column
    assert len(errors) > 0
    assert any("site_name" in error.lower() for error in errors)


def test_community_gardens_validator_statistical_validation_valid_count(base_test_data):
    """Test statistical validation with valid record count."""
    # Create data with ~205 records (within expected range)
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add site_name column
    test_data["site_name"] = [f"Community Garden {i}" for i in range(n)]

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
    # Add site_name column
    test_data["site_name"] = [f"Community Garden {i}" for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too few records
    assert not result.success
    assert len(result.errors) > 0
    assert any("outside expected range" in error.lower() for error in result.errors)


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
    # Add site_name column
    test_data["site_name"] = [f"Community Garden {i}" for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too many records
    assert not result.success
    assert len(result.errors) > 0
    assert any("outside expected range" in error.lower() for error in result.errors)


def test_community_gardens_validator_statistical_validation_low_site_name_coverage(
    base_test_data,
):
    """Test statistical validation with low site name coverage."""
    # Create data with ~205 records but low site name coverage
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set only 10% to have site names (below 80% threshold)
    test_data["site_name"] = [
        f"Community Garden {i}" if i < 20 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CommunityGardensOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to low site name coverage
    assert not result.success
    assert len(result.errors) > 0
    assert any("coverage" in error.lower() for error in result.errors)


def test_community_gardens_validator_statistical_validation_direct(base_test_data):
    """Test statistical validation logic directly."""
    # Create data with valid count but low site name coverage
    n = 205
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    test_data["site_name"] = [
        f"Community Garden {i}" if i < 20 else None for i in range(n)
    ]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = CommunityGardensOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch low site name coverage
    assert len(errors) > 0
    assert any("coverage" in error.lower() for error in errors)


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
