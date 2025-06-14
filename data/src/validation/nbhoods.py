import geopandas as gpd

from .base import BaseValidator


class NeighborhoodsInputValidator(BaseValidator):
    """Validator for access process service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class NeighborhoodsOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
