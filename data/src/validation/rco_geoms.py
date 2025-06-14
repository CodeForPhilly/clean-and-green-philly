import geopandas as gpd

from .base import BaseValidator


class RCOGeomsInputValidator(BaseValidator):
    """Validator for rco geoms service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class RCOGeomsOutputValidator(BaseValidator):
    """Validator for rco geoms service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
