import geopandas as gpd

from .base import BaseValidator


class CityOwnedPropertiesInputValidator(BaseValidator):
    """Validator for access city owned properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CityOwnedPropertiesOutputValidator(BaseValidator):
    """Validator for city owned properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
