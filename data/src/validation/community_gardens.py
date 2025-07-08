import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator, row_count_check

# Define the Community Gardens DataFrame Schema
CommunityGardensSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Vacant status - should be boolean, can be nullable
        "vacant": pa.Column(bool, nullable=True, description="Vacant property status"),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)

# Reference count for community gardens
COMMUNITY_GARDENS_REFERENCE_COUNT = 205

CommunityGardensInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.String, checks=pa.Check(lambda s: s.dropna() != "")),
        "geometry": pa.Column("geometry"),
        "site_name": pa.Column(str, nullable=True),
    },
    checks=row_count_check(COMMUNITY_GARDENS_REFERENCE_COUNT, tolerance=0.1),
    strict=False,
)


class CommunityGardensInputValidator(BaseValidator):
    """Validator for community gardens service input."""

    schema = CommunityGardensInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the community gardens input data."""
        self._print_summary_header("Community Gardens Input Data Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal community gardens: {total_records:,}")

        # Site name statistics
        if "site_name" in gdf.columns:
            non_null_site_names = gdf["site_name"].notna().sum()
            site_name_coverage = (
                (non_null_site_names / total_records) * 100 if total_records > 0 else 0
            )
            print(
                f"Site names with values: {non_null_site_names:,} ({site_name_coverage:.1f}%)"
            )
            print(f"Site names missing: {total_records - non_null_site_names:,}")

        # Unique site names using utility function
        if "site_name" in gdf.columns:
            unique_site_names = gdf["site_name"].nunique()
            print(f"Unique site names: {unique_site_names:,}")

        self._print_summary_footer()


class CommunityGardensOutputValidator(BaseValidator):
    """Validator for community gardens service output with comprehensive statistical validation."""

    schema = CommunityGardensSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["opa_id", "vacant", "geometry"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate vacant column is boolean using utility functions
        if "vacant" in gdf.columns:
            non_null_vacant = gdf["vacant"].dropna()
            if len(non_null_vacant) > 0:
                non_bool_vacant = (
                    ~non_null_vacant.apply(lambda x: isinstance(x, bool))
                ).sum()
                if non_bool_vacant > 0:
                    errors.append(
                        f"Found {non_bool_vacant} non-boolean values in 'vacant' column"
                    )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. Total record count validation - should maintain input dataset size
        total_records = len(gdf)
        if total_records == 0:
            errors.append("Output dataset is empty")

        # 2. Vacant column validation using utility functions
        if "vacant" in gdf.columns:
            non_vacant_count = (~gdf["vacant"]).sum()
            vacant_count = gdf["vacant"].sum()

            # Should have some non-vacant parcels (community gardens)
            if non_vacant_count == 0:
                errors.append(
                    "No parcels marked as non-vacant - expected some community gardens to be identified"
                )

            # Should have reasonable distribution (not all vacant or all non-vacant)
            if vacant_count == 0:
                errors.append(
                    "No vacant parcels found - this seems unlikely for a full property dataset"
                )

            # Use utility function to validate boolean distribution
            # Expect roughly 2 unique values (True/False) for vacant column
            self._validate_unique_count(gdf, "vacant", errors, min_count=1, max_count=2)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the community gardens data."""
        self._print_summary_header("Community Gardens Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Vacant status statistics
        if "vacant" in gdf.columns:
            vacant_count = gdf["vacant"].sum()
            non_vacant_count = (~gdf["vacant"]).sum()
            vacant_percentage = (
                (vacant_count / total_records) * 100 if total_records > 0 else 0
            )
            non_vacant_percentage = (
                (non_vacant_count / total_records) * 100 if total_records > 0 else 0
            )

            print(f"Vacant properties: {vacant_count:,} ({vacant_percentage:.1f}%)")
            print(
                f"Non-vacant properties: {non_vacant_count:,} ({non_vacant_percentage:.1f}%)"
            )

            # Community gardens effect
            print(
                f"\nProperties marked as non-vacant (including community gardens): {non_vacant_count:,}"
            )

        self._print_summary_footer()
