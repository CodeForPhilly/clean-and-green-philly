from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class AccessProcessOutputSchema(DataFrameModel):
    access_process: Series[
        Literal[
            "Private Land Use Agreement",
            "Go through Land Bank",
            "PRA",
            "Do Nothing",
            "Buy Property",
        ]
    ]


class AccessProcessOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = AccessProcessOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
