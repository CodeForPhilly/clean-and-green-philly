import geopandas as gpd

from .base import BaseValidator


class TacticalUrbanismOutputValidator(BaseValidator):
    """Validator for tacitcal urbanism service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
