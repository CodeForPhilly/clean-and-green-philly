import geopandas as gpd
from pandera.pandas import Check, Column, DataFrameSchema

from .base import BaseValidator

output_schema = DataFrameSchema(
    {
        "access_process": Column(
            str,
            checks=Check.isin(
                [
                    "Private Land Use Agreement",
                    "Go through Land Bank",
                    "PRA",
                    "Do Nothing",
                    "Buy Property",
                ]
            ),
        )
    }
)


class AccessProcessOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
