import geopandas as gpd

from .base import BaseValidator


class CommunityGardensInputValidator(BaseValidator):
    """Validator for community gardens service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CommunityGardensOutputValidator(BaseValidator):
    """Validator for community gardens service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
