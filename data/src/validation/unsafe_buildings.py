import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema(
    {"unsafe_buildings": Column(str, checks=Check.isin(["Y", "N"]))}
)


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
