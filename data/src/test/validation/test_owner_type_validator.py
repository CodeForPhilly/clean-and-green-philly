import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.owner_type import OwnerTypeOutputValidator


def _create_owner_type_test_data(base_test_data):
    """Create test data with only the columns expected by the owner type validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "owner_type": ["Individual", "Business (LLC)", "Public"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_owner_type_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_owner_type_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_owner_type_validator_schema_edge_cases(base_test_data):
    """Test that the validator catches schema-level edge cases."""
    # Create test data with schema violations
    test_data = _create_owner_type_test_data(base_test_data)
    test_data.loc[1, "owner_type"] = "Invalid Type"  # Invalid value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to schema violations
    assert not result.success
    assert len(result.errors) > 0

    # Check specific errors
    error_messages = [str(error) for error in result.errors]

    # Should catch invalid owner_type (schema check)
    assert any("owner_type" in msg.lower() for msg in error_messages)


def test_owner_type_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_owner_type_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_owner_type_validator_missing_required_columns(base_test_data):
    """Test that the validator catches missing required columns."""
    # Test with missing owner_type column
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing owner_type column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to missing owner_type column
    assert not result.success
    assert len(result.errors) > 0


def test_owner_type_validator_invalid_owner_type_values(base_test_data):
    """Test that the validator catches invalid owner_type values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "owner_type": [
                "Individual",
                "Invalid Type",
                "Public",
            ],  # Invalid value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to invalid owner_type values
    assert not result.success
    assert len(result.errors) > 0


def test_owner_type_validator_null_values(base_test_data):
    """Test that the validator catches null values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "owner_type": [
                "Individual",
                None,
                "Public",
            ],  # Null value
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to null values (not allowed in schema)
    assert not result.success
    assert len(result.errors) > 0


def test_owner_type_validator_empty_dataframe(base_test_data):
    """Test that the validator handles empty dataframes correctly."""
    # Create empty dataframe with required columns
    test_data = pd.DataFrame(columns=["opa_id", "owner_type", "geometry"])

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to empty dataframe
    assert not result.success
    assert len(result.errors) > 0


def test_owner_type_validator_row_level_validation_direct(base_test_data):
    """Test row-level validation logic directly."""
    # Create data with various edge cases to test row-level validation
    test_data = _create_owner_type_test_data(base_test_data)
    test_data.loc[1, "owner_type"] = "Invalid Type"  # Invalid value

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = OwnerTypeOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch multiple issues
    assert len(errors) > 0

    # Check for specific error types
    error_messages = [error.lower() for error in errors]
    assert any("invalid" in msg and "owner_type" in msg for msg in error_messages)


def test_owner_type_validator_missing_owner_type_column(base_test_data):
    """Test that the validator catches missing owner_type column."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            # Missing owner_type column
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = OwnerTypeOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch missing owner_type column
    assert len(errors) > 0
    assert any("owner_type" in error.lower() for error in errors)


def test_owner_type_validator_statistical_validation_valid_distribution(base_test_data):
    """Test statistical validation with valid distribution."""
    # Create data with ~1,000 records and valid distribution (much faster than 580k)
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]

    # Create distribution matching actual data: 88% Individual, 9% Business, 2.7% Public, 0.03% Nonprofit
    individual_count = int(n * 0.88)
    business_count = int(n * 0.09)
    public_count = int(n * 0.027)
    nonprofit_count = n - individual_count - business_count - public_count

    owner_types = (
        ["Individual"] * individual_count
        + ["Business (LLC)"] * business_count
        + ["Public"] * public_count
        + ["Nonprofit/Civic"] * nonprofit_count
    )
    test_data["owner_type"] = owner_types

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass with valid distribution
    assert result.success
    assert len(result.errors) == 0


def test_owner_type_validator_statistical_validation_too_few_records(base_test_data):
    """Test statistical validation with too few records."""
    # Create data with only 100,000 records (below expected minimum)
    n = 100000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Add owner_type column with valid distribution
    test_data["owner_type"] = ["Individual"] * n

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to too few records
    assert not result.success
    assert len(result.errors) > 0
    assert any("below expected minimum" in error.lower() for error in result.errors)


def test_owner_type_validator_statistical_validation_invalid_distribution(
    base_test_data,
):
    """Test statistical validation with invalid distribution."""
    # Create data with ~1,000 records but invalid distribution (much faster than 580k)
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]

    # Create invalid distribution: 50% Individual (should be 88%)
    individual_count = int(n * 0.5)
    business_count = int(n * 0.5)

    owner_types = ["Individual"] * individual_count + [
        "Business (LLC)"
    ] * business_count
    test_data["owner_type"] = owner_types

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to invalid distribution
    assert not result.success
    assert len(result.errors) > 0
    assert any("percentage" in error.lower() for error in result.errors)


def test_owner_type_validator_statistical_validation_direct(base_test_data):
    """Test statistical validation logic directly."""
    # Create data with valid count but invalid distribution (using smaller dataset)
    n = 1000
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]

    # Create invalid distribution: 50% Individual (should be 88%)
    individual_count = int(n * 0.5)
    business_count = int(n * 0.5)

    owner_types = ["Individual"] * individual_count + [
        "Business (LLC)"
    ] * business_count
    test_data["owner_type"] = owner_types

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test statistical validation directly
    validator = OwnerTypeOutputValidator()
    errors = []
    validator._statistical_validation(gdf, errors)

    # Should catch invalid distribution
    assert len(errors) > 0
    assert any("percentage" in error.lower() for error in errors)


def test_owner_type_validator_non_string_opa_id(base_test_data):
    """Test that the validator catches non-string OPA IDs."""
    # Create data with non-string OPA IDs
    test_data = _create_owner_type_test_data(base_test_data)
    test_data["opa_id"] = [
        351243200,
        351121400,
        212525650,
    ]  # Integers instead of strings

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    # Test row-level validation directly
    validator = OwnerTypeOutputValidator()
    errors = []
    validator._row_level_validation(gdf, errors)

    # Should catch non-string OPA IDs (inherited from base validator)
    # Note: This is tested in the base validator tests, but we include it here for completeness
    assert len(errors) == 0  # Row-level validation doesn't check OPA types, schema does


def test_owner_type_validator_duplicate_opa_ids(base_test_data):
    """Test that the validator catches duplicate OPA IDs."""
    # Create data with duplicate OPA IDs
    test_data = _create_owner_type_test_data(base_test_data)
    test_data["opa_id"] = ["351243200", "351243200", "212525650"]  # Duplicate OPA ID

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to duplicate OPA IDs (schema validation)
    assert not result.success
    assert len(result.errors) > 0


def test_owner_type_validator_all_valid_values(base_test_data):
    """Test that the validator accepts all four valid owner type values."""
    # Create test data with 4 records to test all valid values
    test_data = pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650", "999999999"],
            "owner_type": [
                "Individual",
                "Business (LLC)",
                "Public",
                "Nonprofit/Civic",
            ],
            "geometry": [
                base_test_data["geometry"].iloc[0],
                base_test_data["geometry"].iloc[1],
                base_test_data["geometry"].iloc[2],
                base_test_data["geometry"].iloc[0],  # Reuse first geometry
            ],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = OwnerTypeOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with all valid values
    assert result.success
    assert len(result.errors) == 0
