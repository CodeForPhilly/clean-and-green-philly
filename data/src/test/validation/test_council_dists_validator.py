import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.council_dists import CouncilDistrictsOutputValidator


def _create_council_dists_test_data(base_test_data):
    """Create test data with only the columns expected by the council districts validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "district": ["1", "2", "3"],
            "geometry": base_test_data["geometry"],
        }
    )


def test_council_dists_validator_schema_valid_data(base_test_data):
    """Test that the validator accepts valid data."""
    test_data = _create_council_dists_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CouncilDistrictsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass with valid data
    assert result.success
    assert len(result.errors) == 0


def test_council_dists_validator_invalid_district_values(base_test_data):
    """Test that the validator catches invalid district values."""
    # Create data with invalid district values
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "district": ["1", "2", "11"],  # Invalid district value (11)
            "geometry": base_test_data["geometry"],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CouncilDistrictsOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail due to invalid district values
    assert not result.success
    assert len(result.errors) > 0


def test_council_dists_validator_wrong_district_count():
    """Test that the validator catches wrong number of unique districts."""
    # Create data with only 5 districts instead of 10
    test_data = pd.DataFrame(
        {
            "opa_id": [f"test_{i}" for i in range(100)],
            "district": [str(i % 5 + 1) for i in range(100)],  # Only 5 districts
            "geometry": [Point(-75.089, 40.033) for _ in range(100)],
        }
    )

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = CouncilDistrictsOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail due to wrong district count
    assert not result.success
    assert len(result.errors) > 0
