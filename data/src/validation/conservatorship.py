from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class ConservatorshipOutputSchema(DataFrameModel):
    tactical_urbanism = Series[Literal["Y", "N"]]


class ConservatorshipOutputValidator(BaseValidator):
    """Validator for conservatorship service output."""

    schema = ConservatorshipOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
