from typing import Literal

import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class PriorityLevelOutputSchema(DataFrameModel):
    priority_level: Series[Literal["Low", "Medium", "High"]]


class PriorityLevelOutputValidator(BaseValidator):
    """Validator for priority level service output."""

    schema = PriorityLevelOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
