import geopandas as gpd
from pandera import DataFrameModel

from .base import BaseValidator


class CommunityGardensInputValidator(BaseValidator):
    """Validator for community gardens service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CommunityGardensOutputSchema(DataFrameModel):
    pass

    # Check for vacant column updates in custom check?


class CommunityGardensOutputValidator(BaseValidator):
    """Validator for community gardens service output."""

    schema = CommunityGardensOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
