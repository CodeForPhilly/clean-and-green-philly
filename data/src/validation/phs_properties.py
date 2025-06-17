import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class PHSPropertiesInputValidator(BaseValidator):
    """Validator for PHS properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class PHSPropertiesOutputSchema(DataFrameModel):
    phs_care_program: Series[str]


class PHSPropertiesOutputValidator(BaseValidator):
    """Validator for PHS properties service output."""

    schema = PHSPropertiesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
