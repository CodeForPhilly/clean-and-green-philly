import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, DistributionParams, distribution_check


class LIViolationsInputValidator(BaseValidator):
    """Validator for access process service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class LIViolationsOutputSchema(DataFrameModel):
    all_violations_params = DistributionParams(
        max_value=14, mean=0.0725, std=0.405, q1=0.0, q3=0.0
    )
    open_violations_params = DistributionParams(
        max_value=11, mean=0.0147, std=0.178, q1=0.0, q3=0.0
    )

    all_violations_past_year: Series[int] = Field(
        checks=[*distribution_check(all_violations_params)]
    )
    open_violations_past_year: Series[int] = Field(
        checks=[*distribution_check(open_violations_params)]
    )


class LIViolationsOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = LIViolationsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
