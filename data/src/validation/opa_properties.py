import geopandas as gpd

from .base import BaseValidator


class OPAPropertiesInputValidator(BaseValidator):
    """Validator for opa properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class OPAPropertiesOutputValidator(BaseValidator):
    """Validator for opa properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
