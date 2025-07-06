import geopandas as gpd
import pytest

from src.validation.li_complaints import LIComplaintsOutputValidator


@pytest.fixture
def sample_gdf(base_test_data):
    """Create a sample GeoDataFrame with valid LI complaints KDE data using base test data."""
    # Convert base test data to GeoDataFrame
    gdf = gpd.GeoDataFrame(base_test_data, crs="EPSG:2272")

    # Add LI complaints KDE-specific columns with values that pass validation
    gdf["l_and_i_complaints_density"] = [1e-10, 2e-10, 3e-10]
    gdf["l_and_i_complaints_density_zscore"] = [
        0.05,
        -0.05,
        0.0,
    ]  # Mean close to 0, std reasonable
    gdf["l_and_i_complaints_density_percentile"] = [
        25,
        50,
        95,
    ]  # Include one high-density area
    gdf["l_and_i_complaints_density_label"] = [
        "25th Percentile",
        "50th Percentile",
        "95th Percentile",
    ]

    return gdf


@pytest.fixture
def large_sample_gdf(large_test_data):
    """Create a larger sample GeoDataFrame with realistic distributions for positive tests."""
    # Convert large test data to GeoDataFrame
    gdf = gpd.GeoDataFrame(large_test_data, crs="EPSG:2272")

    # Add LI complaints KDE-specific columns with realistic distributions
    gdf["l_and_i_complaints_density"] = [1e-10 + i * 1e-11 for i in range(len(gdf))]
    gdf["l_and_i_complaints_density_zscore"] = [
        i * 0.2 - 2.9 for i in range(len(gdf))
    ]  # Mean ~0, std ~1
    gdf["l_and_i_complaints_density_percentile"] = [
        int(i * 100 / len(gdf)) for i in range(len(gdf))
    ]  # 0, 1, 2, ..., 100 (integers)
    gdf["l_and_i_complaints_density_label"] = [
        f"{int(i * 100 / len(gdf))}th Percentile" for i in range(len(gdf))
    ]

    return gdf


@pytest.fixture
def validator():
    """Create a LIComplaintsOutputValidator instance."""
    return LIComplaintsOutputValidator()


def test_density_too_high(validator, sample_gdf):
    """Test that validator catches LI complaints density values that are too high."""
    # Set density value above the 1e-8 threshold
    gdf_high_density = sample_gdf.copy()
    gdf_high_density.loc[0, "l_and_i_complaints_density"] = 2e-8  # Above 1e-8 threshold

    result = validator.validate(gdf_high_density)

    assert not result.success
    assert any("density values appear too high" in error for error in result.errors)


def test_negative_density(validator, sample_gdf):
    """Test that validator catches negative LI complaints density values."""
    # Set negative density value
    gdf_negative = sample_gdf.copy()
    gdf_negative.loc[0, "l_and_i_complaints_density"] = -1e-10

    result = validator.validate(gdf_negative)

    assert not result.success
    assert any("should be non-negative" in error for error in result.errors)


def test_density_mean_too_high(validator, sample_gdf):
    """Test that validator catches LI complaints density mean that is too high."""
    # Set all density values to be very high, making the mean too high
    gdf_high_mean = sample_gdf.copy()
    gdf_high_mean["l_and_i_complaints_density"] = [1e-8, 1e-8, 1e-8]  # All at threshold

    result = validator.validate(gdf_high_mean)

    assert not result.success
    assert any(
        "density mean appears outside expected range" in error
        for error in result.errors
    )


def test_density_mean_too_low(validator, sample_gdf):
    """Test that validator catches LI complaints density mean that is too low."""
    # Set all density values to be very low, making the mean too low
    gdf_low_mean = sample_gdf.copy()
    gdf_low_mean["l_and_i_complaints_density"] = [
        1e-13,
        1e-13,
        1e-13,
    ]  # All below 1e-12 threshold

    result = validator.validate(gdf_low_mean)

    assert not result.success
    assert any(
        "density mean appears outside expected range" in error
        for error in result.errors
    )


def test_zscore_mean_too_far_from_zero(validator, sample_gdf):
    """Test that validator catches z-score mean that is too far from 0."""
    # Set z-score values to have a mean far from 0
    gdf_bad_zscore_mean = sample_gdf.copy()
    gdf_bad_zscore_mean["l_and_i_complaints_density_zscore"] = [
        5.0,
        5.0,
        5.0,
    ]  # Mean = 5.0

    result = validator.validate(gdf_bad_zscore_mean)

    assert not result.success
    assert any(
        "z-score mean appears too far from 0" in error for error in result.errors
    )


def test_zscore_std_too_low(validator, sample_gdf):
    """Test that validator catches z-score standard deviation that is too low."""
    # Set z-score values to have very low standard deviation
    gdf_low_zscore_std = sample_gdf.copy()
    gdf_low_zscore_std["l_and_i_complaints_density_zscore"] = [
        0.1,
        0.1,
        0.1,
    ]  # All same value, std ≈ 0

    result = validator.validate(gdf_low_zscore_std)

    assert not result.success
    assert any(
        "z-score standard deviation appears outside expected range" in error
        for error in result.errors
    )


def test_zscore_std_too_high(validator, sample_gdf):
    """Test that validator catches z-score standard deviation that is too high."""
    # Set z-score values to have very high standard deviation
    gdf_high_zscore_std = sample_gdf.copy()
    gdf_high_zscore_std["l_and_i_complaints_density_zscore"] = [
        -10.0,
        0.0,
        10.0,
    ]  # High std

    result = validator.validate(gdf_high_zscore_std)

    assert not result.success
    assert any(
        "z-score standard deviation appears outside expected range" in error
        for error in result.errors
    )


def test_extreme_zscore_outliers(validator, sample_gdf):
    """Test that validator catches extreme z-score outliers beyond ±10."""
    # Set z-score values beyond the ±10 threshold
    gdf_extreme_outliers = sample_gdf.copy()
    gdf_extreme_outliers["l_and_i_complaints_density_zscore"] = [
        15.0,
        0.0,
        -12.0,
    ]  # Beyond ±10

    result = validator.validate(gdf_extreme_outliers)

    assert not result.success
    assert any("extreme z-score outliers" in error for error in result.errors)


def test_high_density_areas_distribution(validator, sample_gdf):
    """Test that validator catches unusual distribution of high-density areas."""
    # Create data with too many high-density areas (more than 20% in top 10%)
    gdf_many_high_density = sample_gdf.copy()
    gdf_many_high_density["l_and_i_complaints_density_percentile"] = [
        95,
        96,
        97,
    ]  # All in top 10%

    result = validator.validate(gdf_many_high_density)

    assert not result.success
    assert any(
        "high-density areas (≥90th percentile) count appears unusual" in error
        for error in result.errors
    )


def test_few_high_density_areas(validator, sample_gdf):
    """Test that validator catches too few high-density areas."""
    # Create data with too few high-density areas (less than 5% in top 10%)
    gdf_few_high_density = sample_gdf.copy()
    gdf_few_high_density["l_and_i_complaints_density_percentile"] = [
        10,
        20,
        30,
    ]  # None in top 10%

    result = validator.validate(gdf_few_high_density)

    assert not result.success
    assert any(
        "high-density areas (≥90th percentile) count appears unusual" in error
        for error in result.errors
    )


def test_missing_required_columns(validator, sample_gdf):
    """Test that validator catches missing required columns."""
    # Remove a required column
    gdf_missing_column = sample_gdf.copy()
    del gdf_missing_column["l_and_i_complaints_density"]

    result = validator.validate(gdf_missing_column)

    print(f"Actual errors: {result.errors}")
    assert not result.success
    assert any("Schema validation failed" in error for error in result.errors)


def test_percentile_out_of_range(validator, sample_gdf):
    """Test that validator catches percentile values outside 0-100 range."""
    # Set percentile value outside valid range
    gdf_bad_percentile = sample_gdf.copy()
    gdf_bad_percentile.loc[0, "l_and_i_complaints_density_percentile"] = (
        150  # Above 100
    )

    result = validator.validate(gdf_bad_percentile)

    assert not result.success
    assert any("Schema validation failed" in error for error in result.errors)


def test_negative_percentile(validator, sample_gdf):
    """Test that validator catches negative percentile values."""
    # Set negative percentile value
    gdf_negative_percentile = sample_gdf.copy()
    gdf_negative_percentile.loc[
        0, "l_and_i_complaints_density_percentile"
    ] = -10  # Below 0

    result = validator.validate(gdf_negative_percentile)

    assert not result.success
    assert any("Schema validation failed" in error for error in result.errors)


def test_narrow_percentile_distribution(validator, sample_gdf):
    """Test that validator catches too narrow percentile distribution."""
    # Set all percentile values to be the same (narrow distribution)
    gdf_narrow_percentile = sample_gdf.copy()
    gdf_narrow_percentile["l_and_i_complaints_density_percentile"] = [
        50,
        50,
        50,
    ]  # All same value

    result = validator.validate(gdf_narrow_percentile)

    assert not result.success
    assert any(
        "z-score standard deviation appears outside expected range" in error
        or "high-density areas (≥90th percentile) count appears unusual" in error
        for error in result.errors
    )


def test_valid_li_complaints_data_passes(validator, large_sample_gdf):
    """Test that valid LI complaints data passes all validation checks."""
    result = validator.validate(large_sample_gdf)

    assert result.success, f"Validation failed with errors: {result.errors}"


def test_realistic_li_complaints_ranges(validator, large_sample_gdf):
    """Test that realistic LI complaints data ranges pass validation."""
    # This test ensures our validation thresholds are reasonable for real data
    result = validator.validate(large_sample_gdf)

    assert result.success, f"Realistic data failed validation: {result.errors}"

    # Verify the data has reasonable statistical properties
    density = large_sample_gdf["l_and_i_complaints_density"]
    zscore = large_sample_gdf["l_and_i_complaints_density_zscore"]
    percentile = large_sample_gdf["l_and_i_complaints_density_percentile"]

    # Check that density values are in reasonable range
    assert density.max() < 1e-8, "Density max should be below threshold"
    assert density.min() >= 0, "Density min should be non-negative"

    # Check that z-score has reasonable distribution
    assert abs(zscore.mean()) < 0.1, "Z-score mean should be close to 0"
    assert 0.5 < zscore.std() < 2.0, "Z-score std should be reasonable"

    # Check that percentiles span full range
    assert percentile.min() >= 0, "Percentile min should be >= 0"
    assert percentile.max() <= 100, "Percentile max should be <= 100"


def test_empty_dataframe_handling(validator):
    """Test that validator handles empty dataframes gracefully."""
    # Create empty GeoDataFrame with required columns and geometry
    empty_gdf = gpd.GeoDataFrame(
        {
            "l_and_i_complaints_density_label": [],
            "l_and_i_complaints_density": [],
            "l_and_i_complaints_density_zscore": [],
            "l_and_i_complaints_density_percentile": [],
            "geometry": [],
        },
        crs="EPSG:2272",
    )

    result = validator.validate(empty_gdf)

    # Should fail due to schema validation (empty dataframes don't have proper dtypes)
    assert not result.success
    assert any("Schema validation failed" in error for error in result.errors)


def test_single_row_dataframe(validator, sample_gdf):
    """Test that validator handles single-row dataframes."""
    # Create single-row dataframe
    single_row_gdf = sample_gdf.head(1)

    result = validator.validate(single_row_gdf)

    # Should pass basic validation but may fail statistical checks
    # This is expected behavior for very small datasets
    if not result.success:
        # Check that errors are related to statistical validation, not structural issues
        assert any(
            "z-score standard deviation" in error or "high-density areas" in error
            for error in result.errors
        ), f"Unexpected errors for single row: {result.errors}"


def test_large_dataset_performance(validator, large_test_data):
    """Test that validator performs well on larger datasets."""
    # Create a larger dataset (1000 rows)
    large_gdf = gpd.GeoDataFrame(large_test_data, crs="EPSG:2272")

    # Add LI complaints KDE columns with realistic distributions
    large_gdf["l_and_i_complaints_density"] = [
        1e-10 + i * 1e-12 for i in range(len(large_gdf))
    ]
    large_gdf["l_and_i_complaints_density_zscore"] = [
        (i - len(large_gdf) / 2) * 0.1 for i in range(len(large_gdf))
    ]  # Mean ~0, std ~1
    large_gdf["l_and_i_complaints_density_percentile"] = [
        int(i * 100 / len(large_gdf)) for i in range(len(large_gdf))
    ]  # 0 to 100 (integers)
    large_gdf["l_and_i_complaints_density_label"] = [
        f"{int(i * 100 / len(large_gdf))}th Percentile" for i in range(len(large_gdf))
    ]

    result = validator.validate(large_gdf)

    assert result.success, f"Large dataset validation failed: {result.errors}"
