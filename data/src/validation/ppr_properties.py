import logging

import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, row_count_check

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PPR_REFERENCE_COUNT = 507

# Input schema for PPR properties
PPRPropertiesInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.String, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
    },
    checks=row_count_check(PPR_REFERENCE_COUNT, tolerance=0.1),
    strict=False,
)


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = PPRPropertiesInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# Consolidated schema with all validation built-in
PPRPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Vacant column - should be boolean, can be nullable
        "vacant": pa.Column(
            nullable=True,
            checks=[
                pa.Check(
                    lambda s: s.dropna().apply(lambda x: isinstance(x, bool)).all(),
                    error="vacant column contains non-boolean values",
                ),
            ],
            description="Whether the property is vacant",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output."""

    schema = PPRPropertiesSchema

    def validate(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Override validate method to add debugging."""
        logger.debug("Starting validation of PPR properties data")
        logger.debug(f"DataFrame shape: {gdf.shape}")
        logger.debug(f"DataFrame columns: {list(gdf.columns)}")
        logger.debug(f"DataFrame dtypes: {gdf.dtypes}")
        logger.debug("DataFrame info:")
        logger.debug(gdf.info())

        if "vacant" in gdf.columns:
            logger.debug(f"Vacant column values: {gdf['vacant'].tolist()}")
            logger.debug(f"Vacant column dtype: {gdf['vacant'].dtype}")
            logger.debug(f"Vacant column type: {type(gdf['vacant'])}")
            logger.debug(f"Vacant column null count: {gdf['vacant'].isnull().sum()}")
            logger.debug(f"Vacant column unique values: {gdf['vacant'].unique()}")
            logger.debug(
                f"Vacant column value types: {[type(val) for val in gdf['vacant']]}"
            )

            # Check each value type
            for i, val in enumerate(gdf["vacant"]):
                logger.debug(
                    f"Vacant[{i}] = {val} (type: {type(val)}, is_bool: {isinstance(val, bool)})"
                )

        # Let's also check what the schema expects
        logger.debug(
            f"Schema vacant column definition: {self.schema.columns['vacant']}"
        )
        logger.debug(f"Schema vacant dtype: {self.schema.columns['vacant'].dtype}")

        result = super().validate(gdf, check_stats)
        logger.debug(f"Validation result: {result.success}")
        if not result.success:
            logger.debug(f"Validation errors: {result.errors}")

        return result

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the PPR properties data."""
        self._print_summary_header("PPR Properties Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Vacant column statistics
        if "vacant" in gdf.columns:
            vacant_count = gdf["vacant"].sum()
            vacant_pct = (
                (vacant_count / total_records) * 100 if total_records > 0 else 0
            )
            print(f"Properties marked as vacant: {vacant_count:,} ({vacant_pct:.1f}%)")
            print(f"Properties marked as not vacant: {total_records - vacant_count:,}")

            # PPR properties should not be marked as vacant
            if vacant_count > 0:
                print(
                    f"⚠️  Warning: {vacant_count} properties are still marked as vacant"
                )

        self._print_summary_footer()
