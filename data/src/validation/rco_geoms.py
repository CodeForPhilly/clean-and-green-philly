import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema

from .base import BaseValidator, no_na_check, unique_value_check


class RCOGeomsInputValidator(BaseValidator):
    """Validator for rco geoms service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


output_schema = DataFrameSchema(
    {
        "rco_names": Column(str, checks=[no_na_check, unique_value_check(800, 900)]),
        "rco_info": Column(str, checks=[no_na_check, unique_value_check(800, 900)]),
    }
)


class RCOGeomsOutputValidator(BaseValidator):
    """Validator for rco geoms service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
