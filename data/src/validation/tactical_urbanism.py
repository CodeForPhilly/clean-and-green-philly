import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Check
from pandera.typing import Series

from .base import BaseValidator


# class TacticalUrbanismOutputSchema(DataFrameModel):
#     tactical_urbanism: Series[Literal["Y", "N"]]


output_schema = DataFrameSchema(
    {"tactical_urbanism": Column(str, checks=Check.isin(["Y", "N"]))}
)


class TacticalUrbanismOutputValidator(BaseValidator):
    """Validator for tacitcal urbanism service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
