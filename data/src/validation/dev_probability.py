from typing import Literal

import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, DistributionParams, distribution_check


class DevProbabilityInputValidator(BaseValidator):
    """Validator for dev probability service input from census block groups."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class DevProbabilityOuputSchema(DataFrameModel):
    permit_counts_params = DistributionParams(
        mean=42.129, std=44.789, max_value=413.000, q1=18.000, q3=46.000
    )

    permit_count: Series[int] = Field(
        checks=[*distribution_check(permit_counts_params)]
    )
    dev_rank: Series[Literal["Low", "Medium", "High"]]


class DevProbabilityOutputValidator(BaseValidator):
    """Validator for dev probability service output."""

    schema = DevProbabilityOuputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
