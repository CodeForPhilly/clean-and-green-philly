import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator


class PWDParcelsOutputSchema(pa.DataFrameModel):
    opa_id: str = pa.Field()
    geometry: geometry = pa.Field()


class PWDParcelsOutputValidator(BaseValidator):
    """Validator for pwd parcels service output."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
