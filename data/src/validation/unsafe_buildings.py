import geopandas as gpd

from .base import BaseValidator


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
