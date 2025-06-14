import geopandas as gpd

from .base import BaseValidator


class PHSPropertiesInputValidator(BaseValidator):
    """Validator for PHS properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PHSPropertiesOutputValidator(BaseValidator):
    """Validator for PHS properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
