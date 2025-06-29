import geopandas as gpd

from .base import BaseValidator


class DevProbabilityInputValidator(BaseValidator):
    """Validator for dev probability service input from census block groups."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class DevProbabilityOutputValidator(BaseValidator):
    """Validator for dev probability service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
