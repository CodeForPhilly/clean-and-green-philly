import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.access_process import AccessProcessOutputValidator


def _create_access_process_test_data(base_test_data):
    """Create test data with only the columns expected by the access process validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": ["Go through Land Bank", "Do Nothing", "Buy Property"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_access_process_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_access_process_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_schema_edge_cases(base_test_data):
    """Test that the validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = _create_access_process_test_data(base_test_data)
    test_data.loc[1, "access_process"] = "Invalid Process"  # Invalid value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch invalid access_process (schema check)
    assert any("access_process" in msg.lower() for msg in error_messages)


def test_access_process_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_access_process_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing access_process column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing access_process column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing access_process column
    assert not result.success
    assert len(result.errors) > 0


def test_access_process_validator_invalid_access_process_values(base_test_data):
    """Test that the validator catches invalid access_process values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": [
                "Go through Land Bank",
                "Invalid Process",
                "Buy Property",
            ],  # Invalid value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to invalid access_process values
    assert not result.success
    assert len(result.errors) > 0


def test_access_process_validator_null_values_allowed(base_test_data):
    """Test that the validator allows null values (NAs are allowed)."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": [
                "Go through Land Bank",
                None,
                "Buy Property",
            ],  # Null value (allowed)
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass since NAs are allowed
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(columns=["opa_id", "access_process", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_access_process_validator_row_level_validation_direct(base_test_data):
    """Test row-level validation logic directly."""
    # Create data with various edge cases to test row-level validation
    test_data = _create_access_process_test_data(base_test_data)
    test_data.loc[1, "access_process"] = "Invalid Process"  # Invalid value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = AccessProcessOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]
    assert any("invalid" in msg and "access_process" in msg for msg in error_messages)


def test_access_process_validator_missing_access_process_column(base_test_data):
    """Test that the validator catches missing access_process column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing access_process column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = AccessProcessOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing access_process column
    assert len(errors) > 0
    assert any("access_process" in error.lower() for error in errors)


def test_access_process_validator_wrong_data_type(base_test_data):
    """Test that the validator catches wrong data types."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": [
                "Go through Land Bank",
                123,  # Wrong type (integer instead of string)
                "Buy Property",
            ],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to wrong data type
    assert not result.success
    assert len(result.errors) > 0

    # Check for specific error types - Pandera schema validation catches this first
    error_messages = [str(error).lower() for error in result.errors]
    assert any("access_process" in msg for msg in error_messages)


def test_access_process_validator_all_valid_values(base_test_data):
    """Test that the validator accepts all valid access process values."""
    # Create test data with only 3 rows to match base_test_data length
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": [
                "Go through Land Bank",
                "Do Nothing",
                "Private Land Use Agreement",
            ],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with all valid values
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_mixed_valid_and_na_values(base_test_data):
    """Test that the validator accepts a mix of valid values and NAs."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "access_process": [
                "Go through Land Bank",
                None,  # NA value
                "Buy Property",
            ],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with mix of valid values and NAs
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_statistical_validation_valid_distribution(
    base_test_data,
):
    """Test statistical validation with valid distribution."""
    # Create data with ~1,000 records and valid distribution
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()

    # Create unique OPA IDs to avoid duplicate validation errors
    test_data["opa_id"] = [f"test_{i:06d}" for i in range(n)]

    # Create realistic access process distribution
    # Most properties should be NA (non-vacant), some should have access processes
    na_count = int(n * 0.8)  # 80% NA
    valid_count = n - na_count

    access_processes = [None] * na_count
    valid_values = [
        "Go through Land Bank",
        "Do Nothing",
        "Private Land Use Agreement",
        "Buy Property",
    ]
    for i in range(valid_count):
        access_processes.append(valid_values[i % len(valid_values)])

    test_data["access_process"] = access_processes

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass statistical validation
    assert result.success
    assert len(result.errors) == 0


def test_access_process_validator_statistical_validation_too_few_records(
    base_test_data,
):
    """Test statistical validation with too few records."""
    # Create data with only 100 records (below minimum)
    n = 100
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()

    # Create unique OPA IDs to avoid duplicate validation errors
    test_data["opa_id"] = [f"test_{i:06d}" for i in range(n)]

    # Add valid access process values
    test_data["access_process"] = ["Go through Land Bank"] * n

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too few records
    assert not result.success
    assert len(result.errors) > 0

    # Check for specific error
    error_messages = [str(error).lower() for error in result.errors]
    assert any("below expected minimum" in msg for msg in error_messages)


def test_access_process_validator_statistical_validation_invalid_distribution(
    base_test_data,
):
    """Test statistical validation with invalid distribution."""
    # Create data with ~1,000 records but all non-NA (unrealistic)
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()

    # Create unique OPA IDs to avoid duplicate validation errors
    test_data["opa_id"] = [f"test_{i:06d}" for i in range(n)]

    # All properties have access processes (no NAs) - unrealistic
    test_data["access_process"] = ["Go through Land Bank"] * n

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to unrealistic distribution (no NAs)
    assert not result.success
    assert len(result.errors) > 0

    # Check for specific error
    error_messages = [str(error).lower() for error in result.errors]
    assert any("na percentage" in msg for msg in error_messages)


def test_access_process_validator_statistical_validation_direct(base_test_data):
    """Test statistical validation logic directly."""
    # Create data with ~1,000 records and valid distribution
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()

    # Create unique OPA IDs to avoid duplicate validation errors
    test_data["opa_id"] = [f"test_{i:06d}" for i in range(n)]

    # Create realistic access process distribution
    na_count = int(n * 0.8)  # 80% NA
    valid_count = n - na_count

    access_processes = [None] * na_count
    valid_values = [
        "Go through Land Bank",
        "Do Nothing",
        "Private Land Use Agreement",
        "Buy Property",
    ]
    for i in range(valid_count):
        access_processes.append(valid_values[i % len(valid_values)])

    test_data["access_process"] = access_processes

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = AccessProcessOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should pass statistical validation
    assert len(errors) == 0


def test_access_process_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string opa_id values."""
    test_data = pd.DataFrame(
        {
            "opa_id": [123, "456", "789"],  # Non-string opa_id
            "access_process": ["Go through Land Bank", "Do Nothing", "Buy Property"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to non-string opa_id
    assert not result.success
    assert len(result.errors) > 0


def test_access_process_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate opa_ids."""
    test_data = pd.DataFrame(
        {
            "opa_id": ["123", "123", "789"],  # Duplicate opa_id
            "access_process": ["Go through Land Bank", "Do Nothing", "Buy Property"],
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = AccessProcessOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate opa_ids
    assert not result.success
    assert len(result.errors) > 0
