import geopandas as gpd

from .base import BaseValidator


class ContigNeighborsOutputValidator(BaseValidator):
    """Validator for contiguous neighbors service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
