import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.config.config import USE_CRS
from src.validation.council_dists import CouncilDistrictsOutputValidator


def test_council_dists_validator_invalid_district_values():
    """Test that the validator catches invalid district values."""
    # Create data with invalid district values
    test_data = pd.DataFrame(
        {
            "opa_id": ["test_1", "test_2", "test_3"],
            "district": ["1", "2", "11"],  # Invalid district value (11)
            "geometry": [Point(-75.089, 40.033) for _ in range(3)],
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
