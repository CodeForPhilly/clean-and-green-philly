from functools import wraps
from typing import Any, Callable

import geopandas as gpd

from ..constants.services import PHILLY_BOUNDARY_URL
from .base_validator import BaseValidator

# Load Philadelphia boundary and convert to EPSG:2272
philly_gdf = gpd.read_file(PHILLY_BOUNDARY_URL)
philly_gdf = philly_gdf.to_crs("EPSG:2272")
PHILLY_BOUNDARY = philly_gdf.geometry.iloc[0]


class GeometryValidator(BaseValidator):
    """
    Validator for geometry-specific constraints in GeoDataFrames.
    Ensures:
    1. CRS is EPSG:2272 (Pennsylvania South State Plane)
    2. All geometries are valid and not null
    3. All geometries are within Philadelphia city limits
    """

    @staticmethod
    def validate(
        func: Callable[..., gpd.GeoDataFrame],
    ) -> Callable[..., gpd.GeoDataFrame]:
        """
        Decorator to validate geometry constraints in GeoDataFrame output.

        Args:
            func: The function that returns a GeoDataFrame

        Returns:
            A wrapped function that validates the output GeoDataFrame
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> gpd.GeoDataFrame:
            # First run base validation
            result = BaseValidator.validate(func)(*args, **kwargs)

            # Check CRS
            if result.crs != "EPSG:2272":
                raise ValueError(f"CRS must be EPSG:2272, got {result.crs}")

            # Check for null geometries
            if result.geometry.isna().any():
                raise ValueError("Found null geometries in the GeoDataFrame")

            # Check geometry validity
            invalid_geoms = ~result.geometry.is_valid
            if invalid_geoms.any():
                invalid_count = invalid_geoms.sum()
                raise ValueError(f"Found {invalid_count} invalid geometries")

            # Check if geometries are within Philadelphia using shapely.contains
            outside_philly = ~result.geometry.apply(
                lambda geom: PHILLY_BOUNDARY.contains(geom)
            )
            if outside_philly.any():
                outside_count = outside_philly.sum()
                raise ValueError(
                    f"Found {outside_count} geometries outside Philadelphia city limits"
                )

            return result

        return wrapper
