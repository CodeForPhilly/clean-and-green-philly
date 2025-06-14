import geopandas as gpd

from .base import BaseValidator


class OwnerTypeOutputValidator(BaseValidator):
    """Validator for owner type service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
