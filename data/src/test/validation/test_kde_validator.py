import geopandas as gpd
import pandas as pd
import pandera.pandas as pa
import pytest
from pandera import Check

from src.validation.base import BaseKDEValidator


class MockKDEValidator(BaseKDEValidator):
    """Mock implementation of BaseKDEValidator for testing purposes."""

    # Override schema to None for testing custom validation logic
    schema = None
    # Override stats threshold for testing with small datasets
    min_stats_threshold = 1

    @property
    def density_label_column(self) -> str:
        return "density_label"

    @property
    def density_column(self) -> str:
        return "density"

    @property
    def density_zscore_column(self) -> str:
        return "density_zscore"

    @property
    def density_percentile_column(self) -> str:
        return "density_percentile"

    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """Simple validation for testing - just check non-negative values."""
        if "density" in gdf.columns:
            density = gdf["density"]
            if density.min() < 0:
                errors.append("Density values should be non-negative")

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Override statistical validation for testing with small datasets."""
        # Check percentile distribution (should be roughly uniform 0-100)
        if "density_percentile" in gdf.columns:
            percentiles = gdf["density_percentile"]

            # Check that percentiles span a reasonable range
            min_percentile = percentiles.min()
            max_percentile = percentiles.max()

            if min_percentile < 0 or max_percentile > 100:
                errors.append(
                    f"Percentile values outside expected range [0, 100]: "
                    f"min={min_percentile:.2f}, max={max_percentile:.2f}"
                )

            # Check that we have a reasonable distribution (not all same value)
            # Use lower threshold for testing
            unique_percentiles = percentiles.nunique()
            if unique_percentiles < 2:  # Lower threshold for small test datasets
                errors.append(
                    f"Percentile distribution appears too narrow: "
                    f"only {unique_percentiles} unique values"
                )


class SchemaTestKDEValidator(BaseKDEValidator):
    """Test implementation that uses the actual schema for testing schema validation."""

    # Override stats threshold for testing with small datasets
    min_stats_threshold = 1

    # Override schema to use static schema for testing
    schema = pa.DataFrameSchema(
        {
            "density_label": pa.Column(str, nullable=False),
            "density": pa.Column(float, nullable=False),
            "density_zscore": pa.Column(float, nullable=False),
            "density_percentile": pa.Column(
                int,
                nullable=False,
                checks=Check.in_range(0, 100, include_min=True, include_max=True),
            ),
        }
    )

    @property
    def density_label_column(self) -> str:
        return "density_label"

    @property
    def density_column(self) -> str:
        return "density"

    @property
    def density_zscore_column(self) -> str:
        return "density_zscore"

    @property
    def density_percentile_column(self) -> str:
        return "density_percentile"

    def _validate_density_ranges(self, gdf: gpd.GeoDataFrame, errors: list):
        """Empty implementation for schema testing."""
        pass

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Override statistical validation for testing with small datasets."""
        # Check percentile distribution (should be roughly uniform 0-100)
        if "density_percentile" in gdf.columns:
            percentiles = gdf["density_percentile"]

            # Check that percentiles span a reasonable range
            min_percentile = percentiles.min()
            max_percentile = percentiles.max()

            if min_percentile < 0 or max_percentile > 100:
                errors.append(
                    f"Percentile values outside expected range [0, 100]: "
                    f"min={min_percentile:.2f}, max={max_percentile:.2f}"
                )

            # Check that we have a reasonable distribution (not all same value)
            # Use lower threshold for testing
            unique_percentiles = percentiles.nunique()
            if unique_percentiles < 2:  # Lower threshold for small test datasets
                errors.append(
                    f"Percentile distribution appears too narrow: "
                    f"only {unique_percentiles} unique values"
                )


@pytest.fixture
def sample_gdf(base_test_data):
    """Create a sample GeoDataFrame with valid KDE data using base test data."""
    # Convert base test data to GeoDataFrame
    gdf = gpd.GeoDataFrame(base_test_data, crs="EPSG:2272")

    # Add KDE-specific columns with generic names
    gdf["density"] = [1e-10, 2e-10, 3e-10]
    gdf["density_zscore"] = [0.5, -0.5, 1.0]
    gdf["density_percentile"] = [25, 50, 75]
    gdf["density_label"] = [
        "25th Percentile",
        "50th Percentile",
        "75th Percentile",
    ]

    return gdf


@pytest.fixture
def large_sample_gdf(base_test_data):
    """Create a larger sample GeoDataFrame with more unique percentile values for statistical validation tests."""
    # Create more test data by duplicating and modifying the base data
    gdf = gpd.GeoDataFrame(base_test_data, crs="EPSG:2272")

    # Duplicate the data to create more rows
    gdf_duplicated = pd.concat([gdf] * 5, ignore_index=True)

    # Add KDE-specific columns with more unique percentile values
    gdf_duplicated["density"] = [1e-10 + i * 1e-11 for i in range(len(gdf_duplicated))]
    gdf_duplicated["density_zscore"] = [
        0.5 + i * 0.1 for i in range(len(gdf_duplicated))
    ]
    gdf_duplicated["density_percentile"] = [
        i * 5 for i in range(len(gdf_duplicated))
    ]  # 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70
    gdf_duplicated["density_label"] = [
        f"{i * 5}th Percentile" for i in range(len(gdf_duplicated))
    ]

    return gdf_duplicated


@pytest.fixture
def validator():
    """Create a MockKDEValidator instance."""
    return MockKDEValidator()


@pytest.fixture
def schema_validator():
    """Create a SchemaTestKDEValidator instance."""
    return SchemaTestKDEValidator()


# Tests for schema validation
def test_schema_missing_columns(schema_validator, sample_gdf):
    """Test that schema validation catches missing required columns."""
    # Remove a required column
    gdf_missing = sample_gdf.drop(columns=["density"])

    result = schema_validator.validate(gdf_missing)

    print("[DEBUG] result.errors:", result.errors)
    assert not result.success
    # Check for schema validation error (pandera generates different error format)
    assert any("Schema validation failed" in error for error in result.errors)


def test_schema_wrong_column_types(schema_validator, sample_gdf):
    """Test that schema validation catches wrong data types."""
    # Change density column to string type
    gdf_wrong_type = sample_gdf.copy()
    gdf_wrong_type["density"] = ["1e-10", "2e-10", "3e-10"]

    result = schema_validator.validate(gdf_wrong_type)

    assert not result.success


def test_schema_percentile_out_of_range(schema_validator, sample_gdf):
    """Test that schema validation catches percentile values outside 0-100 range."""
    # Set percentile value too high
    gdf_high_percentile = sample_gdf.copy()
    gdf_high_percentile.loc[0, "density_percentile"] = 150

    result = schema_validator.validate(gdf_high_percentile)

    assert not result.success


def test_schema_percentile_negative(schema_validator, sample_gdf):
    """Test that schema validation catches negative percentile values."""
    # Set percentile value too low
    gdf_negative_percentile = sample_gdf.copy()
    gdf_negative_percentile.loc[0, "density_percentile"] = -10

    result = schema_validator.validate(gdf_negative_percentile)

    assert not result.success


def test_schema_null_values(schema_validator, sample_gdf):
    """Test that schema validation catches null values in required columns."""
    # Set a null value in density column
    gdf_null = sample_gdf.copy()
    gdf_null.loc[0, "density"] = None

    result = schema_validator.validate(gdf_null)

    assert not result.success


def test_schema_percentile_wrong_type(schema_validator, sample_gdf):
    """Test that schema validation catches percentile column with wrong type."""
    # Change percentile column to float (should be int)
    gdf_wrong_percentile = sample_gdf.copy()
    gdf_wrong_percentile["density_percentile"] = [25.0, 50.0, 75.0]

    result = schema_validator.validate(gdf_wrong_percentile)

    assert not result.success


def test_schema_valid_data_passes(schema_validator, sample_gdf):
    """Test that valid data passes schema validation."""
    result = schema_validator.validate(sample_gdf)

    assert result.success
    assert len(result.errors) == 0


# Tests for custom validation logic (without schema)
def test_missing_columns(validator, sample_gdf):
    """Test that validator catches missing required columns."""
    # Remove a required column
    gdf_missing = sample_gdf.drop(columns=["density"])

    result = validator.validate(gdf_missing)

    assert not result.success
    assert any("Missing required columns" in error for error in result.errors)


def test_empty_dataframe(validator, empty_dataframe):
    """Test that empty dataframe is caught."""
    # Convert to GeoDataFrame and add geometry column
    empty_gdf = gpd.GeoDataFrame(empty_dataframe, crs="EPSG:2272")
    empty_gdf["geometry"] = []

    result = validator.validate(empty_gdf)

    assert not result.success
    assert any("Missing required columns" in error for error in result.errors)


def test_percentile_distribution_validation(validator, sample_gdf):
    """Test that validator catches unusual percentile distributions."""
    # Create data with too few unique percentile values
    gdf_narrow = sample_gdf.copy()
    gdf_narrow["density_percentile"] = [50, 50, 50]  # All same value

    result = validator.validate(gdf_narrow, check_stats=True)

    assert not result.success
    assert any(
        "Percentile distribution appears too narrow" in error for error in result.errors
    )


def test_percentile_range_validation(validator, sample_gdf):
    """Test that validator catches percentile values outside 0-100 range."""
    # Create data with percentile values outside valid range
    gdf_invalid_range = sample_gdf.copy()
    gdf_invalid_range["density_percentile"] = [0, 50, 101]  # 101 is invalid

    result = validator.validate(gdf_invalid_range, check_stats=True)

    assert not result.success
    assert any(
        "Percentile values outside expected range" in error for error in result.errors
    )


def test_negative_density_validation(validator, sample_gdf):
    """Test that custom density validation catches negative values."""
    # Set negative density value
    gdf_negative = sample_gdf.copy()
    gdf_negative.loc[0, "density"] = -1e-10

    result = validator.validate(gdf_negative)

    assert not result.success
    assert any(
        "Density values should be non-negative" in error for error in result.errors
    )


def test_valid_data_passes_custom_validation(validator, sample_gdf):
    """Test that valid data passes custom validation."""
    result = validator.validate(sample_gdf)

    assert result.success
    assert len(result.errors) == 0
