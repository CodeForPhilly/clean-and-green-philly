import geopandas as gpd

from .base import BaseValidator


class TreeCanopyInputValidator(BaseValidator):
    """Validator for tree canopy service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class TreeCanopyOutputValidator(BaseValidator):
    """Validator for tree canopy service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
