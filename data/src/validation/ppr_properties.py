import geopandas as gpd

from .base import BaseValidator


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
