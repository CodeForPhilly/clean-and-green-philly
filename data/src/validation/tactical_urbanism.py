import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator

output_schema = DataFrameSchema(
    {"tactical_urbanism": Column(str, checks=Check.isin(["Y", "N"]))}
)


class TacticalUrbanismOutputValidator(BaseValidator):
    """Validator for tacitcal urbanism service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
