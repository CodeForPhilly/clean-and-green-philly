import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema
from pandera.typing import Series

from .base import BaseValidator


class VacantPropertiesInputValidator(BaseValidator):
    """Validator for vacant properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class VacantPropertiesOutputSchema(DataFrameModel):
    vacant: Series[bool]


output_schema = DataFrameSchema({"vacant": Column(bool)})


class VacantPropertiesOutputValidator(BaseValidator):
    """Validator for vacant properties service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
