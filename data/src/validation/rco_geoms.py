import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator, no_na_check, number_of_unique


class RCOGeomsInputValidator(BaseValidator):
    """Validator for rco geoms service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class RCOGeomsOutputSchema(DataFrameModel):
    rco_names: Series[str] = Field(checks=[no_na_check, number_of_unique(800, 900)])
    rco_info: Series[str] = Field(checks=[no_na_check, number_of_unique(800, 900)])


class RCOGeomsOutputValidator(BaseValidator):
    """Validator for rco geoms service output."""

    schema = RCOGeomsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
