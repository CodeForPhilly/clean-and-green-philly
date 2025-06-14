import geopandas as gpd

from .base import BaseValidator


class GunCrimesOutputValidator(BaseValidator):
    """Validator for gun crimes service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
