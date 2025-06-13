import geopandas as gpd

from .base import BaseValidator


class CouncilDistrictsInputValidator(BaseValidator):
    """Validator for council districts service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CouncilDistrictsOutputValidator(BaseValidator):
    """Validator for council districts service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
