import geopandas as gpd
import pandas as pd

from src.config.config import USE_CRS
from src.validation.park_priority import ParkPriorityOutputValidator


def _create_park_priority_test_data(base_test_data):
    """Create test data with only the columns expected by the park priority validator."""
    return pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "park_priority": [1.5, 4.2, 5.0],
            "geometry": base_test_data["geometry"],
        }
    )


def test_park_priority_validator_row_level_validation(base_test_data):
    """Test row-level validation that works with any dataset size."""
    test_data = _create_park_priority_test_data(base_test_data)
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should pass row-level validation
    assert result.success
    assert len(result.errors) == 0


def test_park_priority_validator_missing_column(base_test_data):
    """Test validation fails when park_priority column is missing."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "geometry": base_test_data["geometry"],
        }
    )
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail validation
    assert not result.success
    assert any("park_priority" in err for err in result.errors)


def test_park_priority_validator_non_numeric_values(base_test_data):
    """Test validation fails when park_priority contains non-numeric values."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "park_priority": [1.5, "bad", 4.0],
            "geometry": base_test_data["geometry"],
        }
    )
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail validation
    assert not result.success
    # Check for Pandera schema validation errors
    error_messages = [str(error) for error in result.errors]
    assert any("park_priority" in msg.lower() for msg in error_messages)


def test_park_priority_validator_out_of_range_values(base_test_data):
    """Test validation fails when park_priority contains values outside [1.0, 5.0]."""
    test_data = pd.DataFrame(
        {
            "opa_id": base_test_data["opa_id"],
            "park_priority": [1.5, 6.0, 4.0],
            "geometry": base_test_data["geometry"],
        }
    )
    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=False)

    # Should fail validation
    assert not result.success
    # Check for Pandera schema validation errors
    error_messages = [str(error) for error in result.errors]
    assert any("park_priority" in msg.lower() for msg in error_messages)


def test_park_priority_validator_statistical_validation(base_test_data):
    """Test statistical validation with larger dataset."""
    # Create larger dataset using base_test_data pattern
    n = 200
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set all values to 1.5 (mean = 1.5, should fail)
    test_data["park_priority"] = [1.5] * n

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail statistical validation (mean too low)
    assert not result.success
    assert any("mean" in err for err in result.errors)


def test_park_priority_validator_low_non_null_percentage(base_test_data):
    """Test validation fails when non-null percentage is below 95%."""
    # Create dataset using base_test_data pattern
    n = 100
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set 50% to 1.5, 50% to None (50% nulls)
    test_data["park_priority"] = [1.5 if i < 50 else None for i in range(n)]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should fail validation (non-null percentage too low)
    assert not result.success
    assert any("non-null percentage" in err for err in result.errors)


def test_park_priority_validator_valid_data(base_test_data):
    """Test validation passes with valid data."""
    # Create valid dataset using base_test_data pattern
    n = 100
    base = base_test_data.copy()
    reps = (n // len(base)) + 1
    test_data = pd.concat([base] * reps, ignore_index=True).iloc[:n].copy()
    # Assign unique opa_id values
    test_data["opa_id"] = [f"test_opa_{i}" for i in range(n)]
    # Set valid values with good statistics
    valid_values = [1.5, 4.2, 5.0, 4.3, 4.1, 4.4, 4.2, 4.3, 4.1, 5.0] * 10
    test_data["park_priority"] = valid_values[:n]

    gdf = gpd.GeoDataFrame(test_data, geometry="geometry", crs=USE_CRS)

    validator = ParkPriorityOutputValidator()
    result = validator.validate(gdf, check_stats=True)

    # Should pass validation
    assert result.success
    assert len(result.errors) == 0
