import geopandas as gpd

from .base import BaseValidator


class DelinquenciesInputValidator(BaseValidator):
    """Validator for delinquencies service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class DelinquenciesOutputValidator(BaseValidator):
    """Validator for delinquencies service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
