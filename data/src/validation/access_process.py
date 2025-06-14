import geopandas as gpd

from .base import BaseValidator


class AccessProcessOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
