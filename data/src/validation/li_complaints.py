import geopandas as gpd

from .base import BaseValidator


class LIComplaintsOutputValidator(BaseValidator):
    """Validator for LI complaints service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
