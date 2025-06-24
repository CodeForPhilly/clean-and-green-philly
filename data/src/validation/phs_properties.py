import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema

from .base import BaseValidator


class PHSPropertiesInputValidator(BaseValidator):
    """Validator for PHS properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema({"phs_care_program": Column(str)})


class PHSPropertiesOutputValidator(BaseValidator):
    """Validator for PHS properties service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
