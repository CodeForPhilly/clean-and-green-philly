import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Check
from pandera.typing import Series

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


# class AccessProcessOutputSchema(DataFrameModel):
#     access_process: Series[
#         Literal[
#             "Private Land Use Agreement",
#             "Go through Land Bank",
#             "PRA",
#             "Do Nothing",
#             "Buy Property",
#         ]
#     ]


class AccessProcessOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
