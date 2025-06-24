import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

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
