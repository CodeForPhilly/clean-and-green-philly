import geopandas as gpd
from pandera import Check, DataFrameModel, Field
from pandas import Series

from .base import BaseValidator, no_na_check, number_of_unique


class NeighborhoodsInputValidator(BaseValidator):
    """Validator for access process service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class NeighborhoodsOutputSchema(DataFrameModel):
    neighborhood: Series[str] = Field(
        checks=[
            no_na_check,
            number_of_unique(130, 190),
        ]
    )


class NeighborhoodsOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = NeighborhoodsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
