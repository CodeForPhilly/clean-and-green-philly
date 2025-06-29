import geopandas as gpd

from .base import BaseValidator


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class VacantPropertiesOutputValidator(BaseValidator):
    """Validator for vacant properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
