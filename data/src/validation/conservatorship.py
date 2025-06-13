import geopandas as gpd

from .base import BaseValidator


class ConservatorshipOutputValidator(BaseValidator):
    """Validator for conservatorship service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
