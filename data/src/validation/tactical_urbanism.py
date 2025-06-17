from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator


class TacticalUrbanismOutputSchema(DataFrameModel):
    tactical_urbanism = Series[Literal["Y", "N"]]


class TacticalUrbanismOutputValidator(BaseValidator):
    """Validator for tacitcal urbanism service output."""

    schema = TacticalUrbanismOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
