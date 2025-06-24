import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema

from .base import BaseValidator


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema({"vacant": Column(bool)})


class VacantPropertiesOutputValidator(BaseValidator):
    """Validator for vacant properties service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
