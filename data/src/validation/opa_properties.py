import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema, Check

from .base import (
    BaseValidator,
    DistributionParams,
    distribution_check,
    unique_check,
    unique_value_check,
)


class OPAPropertiesInputValidator(BaseValidator):
    """Validator for opa properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# class OPAPropertiesOutputSchema(DataFrameModel):
#     market_value_params = DistributionParams(
#         max_value=496284800,
#         mean=395531.7801,
#         std=3080696.836,
#         q1=134200,
#         q3=325300,
#     )

#     sales_params = DistributionParams(
#         max_value=968000000, mean=315032.1791, std=9937629.715, q1=1, q3=180000
#     )

#     opa_id: Series[str] = Field(checks=[unique_check])
#     market_value: Series[float] = Field(
#         checks=[*distribution_check(market_value_params)]
#     )
#     sale_date: Series[str]
#     sale_price: Series[Optional[float]] = Field(
#         checks=[*distribution_check(sales_params)]
#     )
#     parcel_type: Series[Literal["Land", "Building"]]
#     zip_code: Series[str] = Field(checks=[unique_value_check(50, 60)])
#     zoning: Series[str] = Field(checks=[unique_value_check(40, 50)])
#     owner_1: Series[Optional[str]]
#     owner_2: Series[Optional[str]]
#     building_code_description: Series[Optional[str]]
#     standardized_address: Series[str] = Field(
#         checks=[unique_value_check(450000, 800000)]
#     )
#     geometry: Series[BaseGeometry]


market_value_params = DistributionParams(
    max_value=496284800,
    mean=395531.7801,
    std=3080696.836,
    q1=134200,
    q3=325300,
)
sales_params = DistributionParams(
    max_value=968000000, mean=315032.1791, std=9937629.715, q1=1, q3=180000
)

output_schema = DataFrameSchema(
    {
        "opa_id": Column(str, checks=[unique_check]),
        "market_value": Column(
            float, checks=[*distribution_check(market_value_params)]
        ),
        "sale_date": Column(str),
        "sale_price": Column(
            float, checks=[*distribution_check(sales_params)], coerce=True
        ),
        "parcel_type": Column(str, checks=Check.isin(["Land", "Building"])),
        "zip_code": Column(str, checks=[unique_value_check(50, 60)]),
        "zoning": Column(str, checks=[unique_value_check(40, 50)]),
        "owner_1": Column(str, nullable=True),
        "owner_2": Column(str, nullable=True),
        "building_code_description": Column(str, nullable=True),
        "standardized_address": Column(
            str, checks=[unique_value_check(450000, 800000)]
        ),
    }
)


class OPAPropertiesOutputValidator(BaseValidator):
    """Validator for opa properties service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
