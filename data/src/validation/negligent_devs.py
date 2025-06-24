import geopandas as gpd
from pandera.pandas import DataFrameModel, Field, DataFrameSchema, Column
from pandera.typing import Series

from .base import BaseValidator, DistributionParams, distribution_check


# class NegligentDevsOutputSchema(DataFrameModel):
#     total_params = DistributionParams(
#         max_value=14, mean=0.0725, std=0.405, q1=0.000, q3=0.000
#     )

#     vacant_params = DistributionParams(
#         max_value=11, mean=0.0147, std=0.178, q1=0.000, q3=0.000
#     )

#     negligent_dev: Series[bool]
#     n_total_properties_owned: Series[int] = Field(
#         checks=[*distribution_check(total_params)]
#     )
#     n_vacant_properties_owned: Series[int] = Field(
#         checks=[*distribution_check(vacant_params)]
#     )


total_params = DistributionParams(
    max_value=14, mean=0.0725, std=0.405, q1=0.000, q3=0.000
)
vacant_params = DistributionParams(
    max_value=11, mean=0.0147, std=0.178, q1=0.000, q3=0.000
)

output_schema = DataFrameSchema(
    {
        "negligent_dev": Column(bool),
        "n_total_properties_owned": Column(
            int, checks=[*distribution_check(total_params)]
        ),
        "n_vacant_properties_owned": Column(
            int, checks=[*distribution_check(vacant_params)]
        ),
    }
)


class NegligentDevsOutputValidator(BaseValidator):
    """Validator for negligent devs service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
