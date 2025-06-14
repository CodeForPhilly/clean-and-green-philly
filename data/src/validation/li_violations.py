import geopandas as gpd

from .base import BaseValidator


class LIViolationsInputValidator(BaseValidator):
    """Validator for access process service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class LIViolationsOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
