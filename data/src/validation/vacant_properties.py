import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class VacantPropertiesOutputSchema(DataFrameModel):
    vacant: Series[bool]


class VacantPropertiesOutputValidator(BaseValidator):
    """Validator for vacant properties service output."""

    schema = VacantPropertiesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
