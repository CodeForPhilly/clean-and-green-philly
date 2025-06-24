import geopandas as gpd
from pandera.pandas import DataFrameModel, Field, DataFrameSchema, Column
from pandera.typing import Series

from .base import BaseValidator, DistributionParams, distribution_check


# class GunCrimesOutputSchema(DataFrameModel):
#     density_params = DistributionParams(
#         max_value=4.053986503e-10,
#         mean=1.29543552e-10,
#         std=1.031529159e-10,
#         q1=3.707989081e-11,
#         q3=1.964349887e-10,
#     )
#     zscore_params = DistributionParams(
#         max_value=2.675594422,
#         mean=0.0006885340359,
#         std=1.000251016,
#         q1=-0.8959111425,
#         q3=0.6493200041,
#     )
#     percentile_params = DistributionParams(
#         max_value=100, mean=50.24090979, std=28.73554294, q1=25, q3=75
#     )

#     gun_crimes_density: Series[float] = Field(
#         checks=[*distribution_check(density_params)]
#     )
#     gun_crimes_density_zscore: Series[float] = Field(
#         checks=[*distribution_check(zscore_params)]
#     )
#     gun_crimes_density_label: Series[str]
#     gun_crimes_density_percentile: Series[float] = Field(
#         checks=[*distribution_check(percentile_params)]
#     )


density_params = DistributionParams(
    max_value=4.053986503e-10,
    mean=1.29543552e-10,
    std=1.031529159e-10,
    q1=3.707989081e-11,
    q3=1.964349887e-10,
)
zscore_params = DistributionParams(
    max_value=2.675594422,
    mean=0.0006885340359,
    std=1.000251016,
    q1=-0.8959111425,
    q3=0.6493200041,
)
percentile_params = DistributionParams(
    max_value=100, mean=50.24090979, std=28.73554294, q1=25, q3=75
)


output_schema = DataFrameSchema(
    {
        "gun_crimes_density": Column(
            float, checks=[*distribution_check(density_params)]
        ),
        "gun_crimes_density_zscore": Column(
            float, checks=[*distribution_check(zscore_params)]
        ),
        "gun_crimes_density_label": Column(str),
        "gun_crimes_density_percentile": Column(
            float, checks=[*distribution_check(percentile_params)]
        ),
    }
)


class GunCrimesOutputValidator(BaseValidator):
    """Validator for gun crimes service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
