import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Community Gardens DataFrame Schema
CommunityGardensSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Site name - must be string, can be nullable (we don't keep this column)
        "site_name": pa.Column(
            str, nullable=True, description="Community garden site name"
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class CommunityGardensInputValidator(BaseValidator):
    """Validator for community gardens service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CommunityGardensOutputValidator(BaseValidator):
    """Validator for community gardens service output with comprehensive statistical validation."""

    schema = CommunityGardensSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["site_name"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate site_name column
        if "site_name" in gdf.columns:
            # Check for non-string values (excluding nulls)
            non_null_site_names = gdf["site_name"].dropna()
            if len(non_null_site_names) > 0:
                non_string_site_names = (
                    ~non_null_site_names.apply(lambda x: isinstance(x, str))
                ).sum()
                if non_string_site_names > 0:
                    errors.append(
                        f"Found {non_string_site_names} non-string values in 'site_name' column"
                    )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. Total record count validation - expect around 205 community gardens
        total_records = len(gdf)
        if not (180 <= total_records <= 230):
            errors.append(
                f"Community gardens count ({total_records}) outside expected range [180, 230]"
            )

        # 2. Site name coverage validation
        if "site_name" in gdf.columns:
            non_null_site_names = gdf["site_name"].notna().sum()
            site_name_coverage = (
                (non_null_site_names / total_records) * 100 if total_records > 0 else 0
            )

            # Most community gardens should have site names
            if site_name_coverage < 80:
                errors.append(
                    f"Site name coverage ({site_name_coverage:.1f}%) below expected minimum (80%)"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the community gardens data."""
        self._print_summary_header("Community Gardens Statistical Summary", gdf)

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

        # Unique site names
        if "site_name" in gdf.columns:
            unique_site_names = gdf["site_name"].nunique()
            print(f"Unique site names: {unique_site_names:,}")

        self._print_summary_footer()
