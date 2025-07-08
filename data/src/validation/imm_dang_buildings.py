import geopandas as gpd
import pandera.pandas as pa
from pandera import Check

from .base import BaseValidator, row_count_check

# Define the Imminently Dangerous Buildings DataFrame Schema
ImmDangerBuildingsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Imminently dangerous building flag - can have NaN values from LEFT JOIN, so use object dtype
        "imm_dang_building": pa.Column(
            object,  # Use object dtype to handle NaN values from LEFT JOIN
            nullable=True,  # Allow null values from LEFT JOIN
            checks=[
                Check(
                    lambda s: s.dropna().apply(lambda x: isinstance(x, bool)).all(),
                    error="imm_dang_building column contains non-boolean values",
                ),
            ],
            description="Indicates whether the property is categorized as an imminently dangerous building",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)

# Reference count for imminently dangerous buildings
IMM_DANGER_BUILDINGS_REFERENCE_COUNT = 186

ImmDangerBuildingsInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
    },
    checks=row_count_check(IMM_DANGER_BUILDINGS_REFERENCE_COUNT, tolerance=0.1),
    strict=False,
)


class ImmDangerInputValidator(BaseValidator):
    """Validator for imminent danger buildings service input."""

    schema = ImmDangerBuildingsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


output_schema = pa.DataFrameSchema(
    {"unsafe_building": pa.Column(str, checks=pa.Check.isin(["Y", "N"]))}
)


class ImmDangerOutputValidator(BaseValidator):
    """Validator for imminent danger buildings service output."""

    schema = ImmDangerBuildingsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass
