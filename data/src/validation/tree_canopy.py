from typing import Optional
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import (
    BaseValidator,
    DistributionParams,
    distribution_check,
    null_percentage_check,
)


class TreeCanopyInputValidator(BaseValidator):
    """Validator for tree canopy service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class TreeCanopyOutputSchema(DataFrameModel):
    tree_params = DistributionParams(
        max_value=0.4565896114,
        mean=0.1688201897,
        std=0.08536259767,
        q1=0.1155013519,
        q3=0.228886177,
    )

    tree_canopy_gap: Series[Optional[float]] = Field(
        checks=[null_percentage_check(0.9986), *distribution_check(tree_params)]
    )


class TreeCanopyOutputValidator(BaseValidator):
    """Validator for tree canopy service output."""

    schema = TreeCanopyOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
