import geopandas as gpd

from .base import BaseValidator


class DorParcelsInputValidator(BaseValidator):
    """Validator for dor parcelss service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class DorParcelsOutputValidator(BaseValidator):
    """Validator for dor parcelss service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
