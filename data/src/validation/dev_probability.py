import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator, DistributionParams, distribution_check


class DevProbabilityInputValidator(BaseValidator):
    """Validator for dev probability service input from census block groups."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


permit_counts_params = DistributionParams(
    mean=42.129, std=44.789, max_value=413.000, q1=18.000, q3=46.000
)

output_schema = DataFrameSchema(
    {
        "permit_count": Column(int, checks=[*distribution_check(permit_counts_params)]),
        "dev_rank": Column(str, checks=Check.isin(["Low", "Medium", "High"])),
    }
)


class DevProbabilityOutputValidator(BaseValidator):
    """Validator for dev probability service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
