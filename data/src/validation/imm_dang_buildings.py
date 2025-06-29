import geopandas as gpd

from .base import BaseValidator


class ImmDangerInputValidator(BaseValidator):
    """Validator for imminent danger buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class ImmDangerOutputValidator(BaseValidator):
    """Validator for imminent danger buildings service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
