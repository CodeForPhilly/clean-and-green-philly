from typing import Literal, Optional
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
from pandera.pandas import Series, Field, DataFrameModel


from .base import (
    BaseValidator,
    DistributionParams,
    distribution_check,
    unique_value_check,
    unique_check,
)


class OPAPropertiesInputValidator(BaseValidator):
    """Validator for opa properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class OPAPropertiesOutputSchema(DataFrameModel):
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

    opa_id: Series[str] = Field(checks=[unique_check])
    market_value: Series[float] = Field(
        checks=[*distribution_check(market_value_params)]
    )
    sale_date: Series[str] = Field()
    sale_price: Series[Optional[float]] = Field(
        checks=[*distribution_check(sales_params)]
    )
    parcel_type: Series[Literal["Land", "Building"]] = Field()
    zip_code: Series[str] = Field(checks=[unique_value_check(50, 60)])
    zoning: Series[str] = Field(checks=[unique_value_check(40, 50)])
    owner_1: Series[Optional[str]] = Field()
    owner_2: Series[Optional[str]] = Field()
    building_code_description: Series[Optional[str]] = Field()
    standardized_address: Series[str] = Field(
        checks=[unique_value_check(450000, 800000)]
    )
    geometry: Series[BaseGeometry] = Field()


class OPAPropertiesOutputValidator(BaseValidator):
    """Validator for opa properties service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
