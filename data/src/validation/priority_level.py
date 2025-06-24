import geopandas as gpd
from pandera.pandas import DataFrameModel, DataFrameSchema, Column, Check
from pandera.typing import Series

from .base import BaseValidator


# class PriorityLevelOutputSchema(DataFrameModel):
#     priority_level: Series[Literal["Low", "Medium", "High"]]


output_schema = DataFrameSchema(
    {"priority_level": Column(str, checks=Check.isin(["Low", "Medium", "High"]))}
)


class PriorityLevelOutputValidator(BaseValidator):
    """Validator for priority level service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
