import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator


class ImmDangerInputValidator(BaseValidator):
    """Validator for imminent danger buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema(
    {"unsafe_building": Column(str, checks=Check.isin(["Y", "N"]))}
)


class ImmDangerOutputValidator(BaseValidator):
    """Validator for imminent danger buildings service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
