import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Unsafe Buildings DataFrame Schema
UnsafeBuildingsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Unsafe building flag - must be boolean with no NAs
        "unsafe_building": pa.Column(
            bool,
            nullable=False,
            description="Indicates whether the property is categorized as an unsafe building",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = UnsafeBuildingsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass
