import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Imminently Dangerous Buildings DataFrame Schema
ImmDangerBuildingsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Imminently dangerous building flag - must be boolean with no NAs
        "imm_dang_building": pa.Column(
            bool,
            nullable=False,
            description="Indicates whether the property is categorized as an imminently dangerous building",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)


class ImmDangerInputValidator(BaseValidator):
    """Validator for imminent danger buildings service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class ImmDangerOutputValidator(BaseValidator):
    """Validator for imminent danger buildings service output."""

    schema = ImmDangerBuildingsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass
