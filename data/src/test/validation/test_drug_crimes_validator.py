import geopandas as gpd
import pytest

from src.validation.drug_crimes import DrugCrimesOutputValidator


@pytest.fixture
def sample_gdf(base_test_data):
    """Create a sample GeoDataFrame with valid drug crime KDE data using base test data."""
    # Convert base test data to GeoDataFrame
    gdf = gpd.GeoDataFrame(base_test_data, crs="EPSG:2272")

    # Add drug crime KDE-specific columns with values that pass validation
    gdf["drug_crimes_density"] = [1e-10, 2e-10, 3e-10]
    gdf["drug_crimes_density_zscore"] = [
        0.05,
        -0.05,
        0.0,
    ]  # Mean close to 0, std reasonable
    gdf["drug_crimes_density_percentile"] = [
        25,
        50,
        95,
    ]  # Include one high-density area
    gdf["drug_crimes_density_label"] = [
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

    # Add drug crime KDE-specific columns with realistic distributions
    gdf["drug_crimes_density"] = [1e-10 + i * 1e-11 for i in range(len(gdf))]
    gdf["drug_crimes_density_zscore"] = [
        i * 0.2 - 2.9 for i in range(len(gdf))
    ]  # Mean ~0, std ~1
    gdf["drug_crimes_density_percentile"] = [
        i * 3.45 for i in range(len(gdf))
    ]  # 0, 3.45, 6.9, ..., 100
    gdf["drug_crimes_density_label"] = [
        f"{int(i * 3.45)}th Percentile" for i in range(len(gdf))
    ]

    return gdf


@pytest.fixture
def validator():
    """Create a DrugCrimesOutputValidator instance."""
    return DrugCrimesOutputValidator()


def test_density_too_high(validator, sample_gdf):
    """Test that validator catches drug crime density values that are too high."""
    # Set density value above the 1e-6 threshold
    gdf_high_density = sample_gdf.copy()
    gdf_high_density.loc[0, "drug_crimes_density"] = 2e-6  # Above 1e-6 threshold

    result = validator.validate(gdf_high_density)

    assert not result.success
    assert any("density values appear too high" in error for error in result.errors)


def test_negative_density(validator, sample_gdf):
    """Test that validator catches negative drug crime density values."""
    # Set negative density value
    gdf_negative = sample_gdf.copy()
    gdf_negative.loc[0, "drug_crimes_density"] = -1e-10

    result = validator.validate(gdf_negative)

    assert not result.success
    assert any("should be non-negative" in error for error in result.errors)


def test_density_mean_too_high(validator, sample_gdf):
    """Test that validator catches drug crime density mean that is too high."""
    # Set all density values to be very high, making the mean too high
    gdf_high_mean = sample_gdf.copy()
    gdf_high_mean["drug_crimes_density"] = [1e-6, 1e-6, 1e-6]  # All at threshold

    result = validator.validate(gdf_high_mean)

    assert not result.success
    assert any(
        "density mean appears outside expected range" in error
        for error in result.errors
    )


def test_density_mean_too_low(validator, sample_gdf):
    """Test that validator catches drug crime density mean that is too low."""
    # Set all density values to be very low, making the mean too low
    gdf_low_mean = sample_gdf.copy()
    gdf_low_mean["drug_crimes_density"] = [
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
    gdf_bad_zscore_mean["drug_crimes_density_zscore"] = [5.0, 5.0, 5.0]  # Mean = 5.0

    result = validator.validate(gdf_bad_zscore_mean)

    assert not result.success
    assert any(
        "z-score mean appears too far from 0" in error for error in result.errors
    )


def test_zscore_std_too_low(validator, sample_gdf):
    """Test that validator catches z-score standard deviation that is too low."""
    # Set z-score values to have very low standard deviation
    gdf_low_zscore_std = sample_gdf.copy()
    gdf_low_zscore_std["drug_crimes_density_zscore"] = [
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
    gdf_high_zscore_std["drug_crimes_density_zscore"] = [-10.0, 0.0, 10.0]  # High std

    result = validator.validate(gdf_high_zscore_std)

    assert not result.success
    assert any(
        "z-score standard deviation appears outside expected range" in error
        for error in result.errors
    )


def test_extreme_zscore_outliers(validator, large_sample_gdf):
    """Test that validator catches extreme z-score outliers beyond ±75."""
    # Use large dataset with realistic distributions, then modify z-scores to be extreme outliers
    gdf_extreme_outliers = large_sample_gdf.copy()
    # Set z-score values beyond the ±75 threshold while keeping mean and std reasonable
    gdf_extreme_outliers["drug_crimes_density_zscore"] = [80.0, 0.0, -78.0] + [
        i * 0.1 - 1.45 for i in range(3, len(gdf_extreme_outliers))
    ]

    result = validator.validate(gdf_extreme_outliers)

    assert not result.success
    assert any("extreme z-score outliers" in error for error in result.errors)


def test_high_density_areas_distribution(validator, sample_gdf):
    """Test that validator catches unusual distribution of high-density areas."""
    # Create data with too many high-density areas (more than 20% in top 10%)
    gdf_many_high_density = sample_gdf.copy()
    gdf_many_high_density["drug_crimes_density_percentile"] = [
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
    gdf_few_high_density["drug_crimes_density_percentile"] = [
        10,
        20,
        30,
    ]  # All in bottom 30%

    result = validator.validate(gdf_few_high_density)

    assert not result.success
    assert any(
        "high-density areas (≥90th percentile) count appears unusual" in error
        for error in result.errors
    )


def test_valid_drug_crime_data_passes(validator, large_sample_gdf):
    """Test that valid drug crime data passes all validation."""
    result = validator.validate(large_sample_gdf)

    assert result.success
    assert len(result.errors) == 0


def test_realistic_drug_crime_ranges(validator, large_sample_gdf):
    """Test that realistic drug crime density and z-score ranges pass validation."""
    # Use realistic values based on the actual statistics provided
    gdf_realistic = large_sample_gdf.copy()
    gdf_realistic["drug_crimes_density"] = [
        1e-10 + i * 1e-11 for i in range(len(gdf_realistic))
    ]  # Realistic density range
    gdf_realistic["drug_crimes_density_zscore"] = [
        i * 0.1 - 1.45 for i in range(len(gdf_realistic))
    ]  # Realistic z-score range with mean ~0, std ~1
    gdf_realistic["drug_crimes_density_percentile"] = [
        i * 3.33 for i in range(len(gdf_realistic))
    ]  # Realistic percentiles (0, 3.33, 6.66, ..., 96.66)

    result = validator.validate(gdf_realistic)

    assert result.success
    assert len(result.errors) == 0
