import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Field
from pandera.typing import Series

from .base import BaseValidator, DistributionParams, distribution_check


params = DistributionParams(max_value=49, mean=2.566, std=4.873, q1=0.000, q3=3.000)
output_schema = DataFrameSchema(
    {"n_contiguous": Column(int, checks=[*distribution_check(params)], coerce=True)}
)


# class ContigNeighborsOutputSchema(DataFrameModel):
#     n_contiguous: Series[int] = Field(checks=[*distribution_check(params)])

#     # NAs possible add to distribution check


class ContigNeighborsOutputValidator(BaseValidator):
    """Validator for contiguous neighbors service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
