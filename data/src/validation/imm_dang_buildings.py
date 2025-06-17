from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class ImmDangerInputValidator(BaseValidator):
    """Validator for imminent danger buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class ImmDangerOutputSchema(DataFrameModel):
    unsafe_building: Series[Literal["Y", "N"]]


class ImmDangerOutputValidator(BaseValidator):
    """Validator for imminent danger buildings service output."""

    schema = ImmDangerOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
