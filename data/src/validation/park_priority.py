import geopandas as gpd

from .base import BaseValidator


class ParkPriorityOutputValidator(BaseValidator):
    """Validator for park priority service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
