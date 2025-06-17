import geopandas as gpd
from pandera import DataFrameModel

from .base import BaseValidator


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PPRPropertiesOutputSchema(DataFrameModel):
    pass

    # Check for vacant column updates in custom check?


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output."""

    schema = PPRPropertiesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
