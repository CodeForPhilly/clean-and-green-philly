import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel
from shapely.geometry.base import BaseGeometry

from .base import BaseValidator


class PWDParcelsOutputSchema(DataFrameModel):
    geometry: Series[BaseGeometry]


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for pwd parcels service output."""

    schema = PWDParcelsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
