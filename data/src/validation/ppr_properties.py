import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the PPR Properties DataFrame Schema
PPRPropertiesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Public name - must be string, can be nullable (we don't keep this column)
        "public_name": pa.Column(
            str, nullable=True, description="PPR property public name"
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class PPRPropertiesInputValidator(BaseValidator):
    """Validator for PPR properties service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class PPRPropertiesOutputValidator(BaseValidator):
    """Validator for PPR properties service output with comprehensive statistical validation."""

    schema = PPRPropertiesSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["public_name"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate public_name column
        if "public_name" in gdf.columns:
            # Check for non-string values (excluding nulls)
            non_null_public_names = gdf["public_name"].dropna()
            if len(non_null_public_names) > 0:
                non_string_public_names = (
                    ~non_null_public_names.apply(lambda x: isinstance(x, str))
                ).sum()
                if non_string_public_names > 0:
                    errors.append(
                        f"Found {non_string_public_names} non-string values in 'public_name' column"
                    )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. Total record count validation - expect around 507 PPR properties
        total_records = len(gdf)
        if not (450 <= total_records <= 550):
            errors.append(
                f"PPR properties count ({total_records}) outside expected range [450, 550]"
            )

        # 2. Public name coverage validation
        if "public_name" in gdf.columns:
            non_null_public_names = gdf["public_name"].notna().sum()
            public_name_coverage = (
                (non_null_public_names / total_records) * 100
                if total_records > 0
                else 0
            )

            # Most PPR properties should have public names
            if public_name_coverage < 80:
                errors.append(
                    f"Public name coverage ({public_name_coverage:.1f}%) below expected minimum (80%)"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the PPR properties data."""
        self._print_summary_header("PPR Properties Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal PPR properties: {total_records:,}")

        # Public name statistics
        if "public_name" in gdf.columns:
            non_null_public_names = gdf["public_name"].notna().sum()
            public_name_coverage = (
                (non_null_public_names / total_records) * 100
                if total_records > 0
                else 0
            )
            print(
                f"Public names with values: {non_null_public_names:,} ({public_name_coverage:.1f}%)"
            )
            print(f"Public names missing: {total_records - non_null_public_names:,}")

        # Unique public names
        if "public_name" in gdf.columns:
            unique_public_names = gdf["public_name"].nunique()
            print(f"Unique public names: {unique_public_names:,}")

        self._print_summary_footer()
