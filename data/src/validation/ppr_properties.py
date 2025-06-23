import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PPRPropertiesOutputSchema(DataFrameModel):
    vacant: Series[bool]


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output."""

    schema = PPRPropertiesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
