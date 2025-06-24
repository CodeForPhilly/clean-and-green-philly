import geopandas as gpd

from .base import BaseValidator


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for pwd parcels service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
