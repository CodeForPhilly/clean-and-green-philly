import geopandas as gpd
from pandera.pandas import DataFrameModel, DataFrameSchema, Column
from pandera.typing import Series

from .base import BaseValidator


# class ParkPriorityOutputSchema(DataFrameModel):
#     park_priority: Series[str]


output_schema = DataFrameSchema({"park_priority": Column(str)})


class ParkPriorityOutputValidator(BaseValidator):
    """Validator for park priority service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
