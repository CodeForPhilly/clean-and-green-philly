import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator

output_schema = DataFrameSchema(
    {"priority_level": Column(str, checks=Check.isin(["Low", "Medium", "High"]))}
)


class PriorityLevelOutputValidator(BaseValidator):
    """Validator for priority level service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
