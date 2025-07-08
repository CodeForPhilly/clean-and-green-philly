import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, row_count_check

# Define the RCO Geoms DataFrame Schema
RCOGeomsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # RCO info - must be string with no NAs
        "rco_info": pa.Column(str, nullable=False, description="RCO information"),
        # RCO names - must be string with no NAs
        "rco_names": pa.Column(str, nullable=False, description="RCO names"),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=False,
)

# Reference count for RCO geoms
RCO_GEOMS_REFERENCE_COUNT = 257

RCOGeomsInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
        "organization_name": pa.Column(str),
        "organization_address": pa.Column(str),
        "primary_email": pa.Column(str),
        "primary_phone": pa.Column(str),
    },
    checks=row_count_check(RCO_GEOMS_REFERENCE_COUNT, tolerance=0.1),
    strict=False,
)


class RCOGeomsInputValidator(BaseValidator):
    """Validator for rco geoms service input."""

    schema = RCOGeomsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class RCOGeomsOutputValidator(BaseValidator):
    """Validator for rco geoms service output with statistical validation."""

    schema = RCOGeomsSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""
        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)
        # No additional row-level validation needed for RCO geoms

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""
        # RCO info count validation - should be 800-900 unique values
        if "rco_info" in gdf.columns:
            self._validate_unique_count(
                gdf, "rco_info", errors, min_count=800, max_count=900
            )

        # RCO names count validation - should be 800-900 unique values
        if "rco_names" in gdf.columns:
            self._validate_unique_count(
                gdf, "rco_names", errors, min_count=800, max_count=900
            )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the RCO geoms data."""
        self._print_summary_header("RCO Geoms Statistical Summary", gdf)

        # RCO info distribution
        if "rco_info" in gdf.columns:
            rco_info_dist = gdf["rco_info"].value_counts().sort_index()
            print("\nRCO Info Distribution (Top 20):")
            for rco_info, count in rco_info_dist.head(20).items():
                pct = (count / len(gdf)) * 100
                print(f"  {rco_info}: {count:,} ({pct:.1f}%)")

            # Unique RCO info count
            unique_rco_info_count = gdf["rco_info"].nunique()
            print(f"\nUnique RCO info values: {unique_rco_info_count}")

            # Show total number of RCO info values if more than 20
            if len(rco_info_dist) > 20:
                print(f"Total RCO info values: {len(rco_info_dist)}")

        # RCO names distribution
        if "rco_names" in gdf.columns:
            rco_names_dist = gdf["rco_names"].value_counts().sort_index()
            print("\nRCO Names Distribution (Top 20):")
            for rco_names, count in rco_names_dist.head(20).items():
                pct = (count / len(gdf)) * 100
                print(f"  {rco_names}: {count:,} ({pct:.1f}%)")

            # Unique RCO names count
            unique_rco_names_count = gdf["rco_names"].nunique()
            print(f"\nUnique RCO names values: {unique_rco_names_count}")

            # Show total number of RCO names values if more than 20
            if len(rco_names_dist) > 20:
                print(f"Total RCO names values: {len(rco_names_dist)}")

        self._print_summary_footer()
