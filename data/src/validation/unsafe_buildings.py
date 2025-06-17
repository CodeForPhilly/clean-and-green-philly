from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class UnsafeBuildingsOutputSchema(DataFrameModel):
    unsafe_building: Series[Literal["Y", "N"]]


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = UnsafeBuildingsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
