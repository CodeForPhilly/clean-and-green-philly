import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel

from .base import BaseValidator


class ParkPriorityOutputSchema(DataFrameModel):
    park_priority: Series[str]


class ParkPriorityOutputValidator(BaseValidator):
    """Validator for park priority service output."""

    schema = ParkPriorityOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
