import geopandas as gpd
from pandera.pandas import DataFrameModel, Field, DataFrameSchema, Column, Check
from pandera.typing import Series

from .base import BaseValidator, DistributionParams, distribution_check


class DelinquenciesInputValidator(BaseValidator):
    """Validator for delinquencies service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


total_due_params = DistributionParams(
    max_value=951046.42,
    mean=7291.178875,
    std=14821.81088,
    q1=873.21,
    q3=8301.53,
)
total_assessment_params = DistributionParams(
    max_value=137576900,
    mean=146337.2527,
    std=1474304.277,
    q1=29300,
    q3=116800,
)
num_year_owed_params = DistributionParams(
    max_value=45, mean=7.641, std=8.923, q1=2.000, q3=10.000
)

output_schema = DataFrameSchema(
    {
        "total_due": Column(
            float, checks=[*distribution_check(total_due_params)], coerce=True
        ),
        "most_recent_year_owed": Column(str),
        "num_years_owed": Column(
            int, checks=[*distribution_check(num_year_owed_params)], coerce=True
        ),
        "payment_agreement": Column(bool, coerce=True),
        "is_actionable": Column(bool),
        "sheriff_sale": Column(str, checks=Check.isin(["Y", "N"])),
        "total_assessment": Column(
            float, checks=[*distribution_check(total_assessment_params)], coerce=True
        ),
    }
)


# class DelinquenciesOutputSchema(DataFrameModel):
#     total_due: Series[float | Literal["NA"]] = Field(
#         checks=[*distribution_check(total_due_params)]
#     )
#     most_recent_year_owed: Series[str]
#     num_years_owed: Series[int | Literal["NA"]] = Field(
#         checks=[*distribution_check(num_year_owed_params)]
#     )
#     payment_agreement: Series[bool | Literal["NA"]]
#     is_actionable: Series[bool]
#     sheriff_sale: Series[Literal["Y", "N"]]
#     total_assessment: Series[float | Literal["NA"]] = Field(
#         checks=[*distribution_check(total_assessment_params)]
#     )


class DelinquenciesOutputValidator(BaseValidator):
    """Validator for delinquencies service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
