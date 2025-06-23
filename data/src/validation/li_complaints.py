import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, DistributionParams, distribution_check


class LIComplaintsOutputSchema(DataFrameModel):
    density_params = DistributionParams(
        max_value=1.981722964e-09,
        mean=4.617083307e-10,
        std=3.406920315e-10,
        q1=1.887178786e-10,
        q3=6.576408078e-10,
    )
    zscore_params = DistributionParams(
        max_value=4.463325725,
        mean=0.00136364009,
        std=1.000092298,
        q1=0.7999924918,
        q3=0.5765181582,
    )
    percentile_params = DistributionParams(
        max_value=100, mean=50.54374968, std=28.85822657, q1=26, q3=76
    )

    l_and_i_complaints_density: Series[float] = Field(
        checks=[*distribution_check(density_params)]
    )
    l_and_i_complaints_density_zscore: Series[float] = Field(
        checks=[*distribution_check(zscore_params)]
    )
    l_and_i_complaints_density_label: Series[str]
    l_and_i_complaints_density_percentile: Series[float] = Field(
        checks=[*distribution_check(percentile_params)]
    )


class LIComplaintsOutputValidator(BaseValidator):
    """Validator for LI complaints service output."""

    schema = LIComplaintsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
