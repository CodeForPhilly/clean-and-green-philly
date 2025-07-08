import geopandas as gpd
import pandera.pandas as pa
from pandera import Check

from .base import BaseValidator, row_count_check

# Define the Unsafe Buildings DataFrame Schema
UnsafeBuildingsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Unsafe building flag - can have NaN values from LEFT JOIN, so use object dtype
        "unsafe_building": pa.Column(
            object,  # Use object dtype to handle NaN values from LEFT JOIN
            nullable=True,  # Allow null values from LEFT JOIN
            checks=[
                Check(
                    lambda s: s.dropna().apply(lambda x: isinstance(x, bool)).all(),
                    error="unsafe_building column contains non-boolean values",
                ),
            ],
            description="Indicates whether the property is categorized as an unsafe building",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)

# Reference count for unsafe buildings
UNSAFE_BUILDINGS_REFERENCE_COUNT = 3520

UnsafeBuildingsInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.String, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
    },
    checks=row_count_check(UNSAFE_BUILDINGS_REFERENCE_COUNT, tolerance=0.1),
    strict=False,
)


class UnsafeBuildingsInputValidator(BaseValidator):
    """Validator for unsafe buildings service input."""

    schema = UnsafeBuildingsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class UnsafeBuildingsOutputValidator(BaseValidator):
    """Validator for unsafe buildings service output."""

    schema = UnsafeBuildingsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass
