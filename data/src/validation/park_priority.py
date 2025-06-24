import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema

from .base import BaseValidator

output_schema = DataFrameSchema({"park_priority": Column(str)})


class ParkPriorityOutputValidator(BaseValidator):
    """Validator for park priority service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
