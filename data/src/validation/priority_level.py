import geopandas as gpd

from .base import BaseValidator


class PriorityLevelOutputValidator(BaseValidator):
    """Validator for priority level service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
