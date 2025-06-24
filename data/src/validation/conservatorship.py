import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Check
from pandera.typing import Series

from .base import BaseValidator


output_schema = DataFrameSchema(
    {"tactical_urbanism": Column(str, checks=Check.isin(["Y", "N"]))}
)


# class ConservatorshipOutputSchema(DataFrameModel):
#     tactical_urbanism: Series[Literal["Y", "N"]]


class ConservatorshipOutputValidator(BaseValidator):
    """Validator for conservatorship service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
