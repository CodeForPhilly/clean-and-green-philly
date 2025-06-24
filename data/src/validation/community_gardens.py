import geopandas as gpd
from pandera.pandas import Column, DataFrameModel, DataFrameSchema
from pandera.typing import Series

from .base import BaseValidator


class CommunityGardensInputValidator(BaseValidator):
    """Validator for community gardens service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema({"vacant": Column(bool)})


# class CommunityGardensOutputSchema(DataFrameModel):
#     vacant: Series[bool]


class CommunityGardensOutputValidator(BaseValidator):
    """Validator for community gardens service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
