import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema, Field
from pandera.typing import Series

from .base import BaseValidator, no_na_check, unique_value_check


class NeighborhoodsInputValidator(BaseValidator):
    """Validator for access process service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# class NeighborhoodsOutputSchema(DataFrameModel):
#     neighborhood: Series[str] = Field(
#         checks=[
#             no_na_check,
#             number_of_unique(130, 190),
#         ]
#     )


output_schema = DataFrameSchema(
    {"neighborhood": Column(str, checks=[no_na_check, unique_value_check(130, 190)])}
)


class NeighborhoodsOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
