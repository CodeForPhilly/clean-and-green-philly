import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Check
from pandera.typing import Series

from .base import BaseValidator


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# class UnsafeBuildingsOutputSchema(DataFrameModel):
#     unsafe_building: Series[Literal["Y", "N"]]


output_schema = DataFrameSchema(
    {"unsafe_buildings": Column(str, checks=Check.isin(["Y", "N"]))}
)


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
