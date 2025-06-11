import geopandas as gpd

from .base import BaseValidator


class NegligentDevsOutputValidator(BaseValidator):
    """Validator for negligent devs service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
