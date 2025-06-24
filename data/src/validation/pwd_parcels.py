import geopandas as gpd
from pandera.pandas import DataFrameModel, DataFrameSchema, Column
from pandera.typing import Series

from .base import BaseValidator


# class PWDParcelsOutputSchema(DataFrameModel):
#     geometry: Series[BaseGeometry]


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for pwd parcels service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
