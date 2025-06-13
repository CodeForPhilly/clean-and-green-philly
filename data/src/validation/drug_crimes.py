import geopandas as gpd

from .base import BaseValidator


class DrugCrimesOutputValidator(BaseValidator):
    """Validator for drug crimes service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
