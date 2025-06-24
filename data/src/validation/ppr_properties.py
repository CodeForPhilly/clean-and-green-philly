import geopandas as gpd
from pandera.pandas import DataFrameModel, DataFrameSchema, Column
from pandera.typing import Series

from .base import BaseValidator


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# class PPRPropertiesOutputSchema(DataFrameModel):
#     vacant: Series[bool]


output_schema = DataFrameSchema({"vacant": Column(bool)})


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
