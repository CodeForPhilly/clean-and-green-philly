import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, DistributionParams, distribution_check


class ContigNeighborsOutputSchema(DataFrameModel):
    params = DistributionParams(max_value=49, mean=2.566, std=4.873, q1=0.000, q3=3.000)

    n_contiguous: Series[int] = Field(checks=[*distribution_check(params)])

    # NAs possible add to distribution check


class ContigNeighborsOutputValidator(BaseValidator):
    """Validator for contiguous neighbors service output."""

    schema = ContigNeighborsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
