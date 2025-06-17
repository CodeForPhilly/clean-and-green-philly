from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, no_na_check


class OwnerTypeOutputSchema(DataFrameModel):
    owner_type: Series[Literal["Individual", "Business (LLC)", "Public"]] = Field(
        checks=[no_na_check]
    )

    # Additional check for number in each category?


class OwnerTypeOutputValidator(BaseValidator):
    """Validator for owner type service output."""

    schema = OwnerTypeOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
