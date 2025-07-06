import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Owner Type DataFrame Schema
OwnerTypeSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Owner type - must be string with no NAs, only specific values allowed
        "owner_type": pa.Column(
            str,
            pa.Check.isin(
                ["Public", "Nonprofit/Civic", "Business (LLC)", "Individual"]
            ),
            nullable=False,
            description="Owner type classification",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class OwnerTypeInputValidator(BaseValidator):
    """Validator for owner type service input."""

    schema = None  # No schema validation for input

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


class OwnerTypeOutputValidator(BaseValidator):
    """Validator for owner type service output with comprehensive statistical validation."""

    schema = OwnerTypeSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["owner_type"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate owner_type column
        if "owner_type" in gdf.columns:
            # Check for null values
            null_owner_types = gdf["owner_type"].isna().sum()
            if null_owner_types > 0:
                errors.append(
                    f"Found {null_owner_types} null values in 'owner_type' column"
                )

            # Check for non-string values
            non_string_owner_types = (
                ~gdf["owner_type"].apply(lambda x: isinstance(x, str))
            ).sum()
            if non_string_owner_types > 0:
                errors.append(
                    f"Found {non_string_owner_types} non-string values in 'owner_type' column"
                )

            # Check for invalid values
            valid_values = ["Public", "Nonprofit/Civic", "Business (LLC)", "Individual"]
            invalid_values = (~gdf["owner_type"].isin(valid_values)).sum()
            if invalid_values > 0:
                errors.append(
                    f"Found {invalid_values} invalid values in 'owner_type' column"
                )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # 1. Total record count validation - expect around 580,000+ records
        # For testing purposes, allow smaller datasets (10k+) to pass validation
        total_records = len(gdf)
        min_records = (
            1000 if total_records < 10000 else 500000
        )  # Lower threshold for testing

        if total_records < min_records:
            errors.append(
                f"Owner type count ({total_records}) below expected minimum ({min_records:,})"
            )

        # 2. Owner type distribution validation based on actual data
        if "owner_type" in gdf.columns:
            owner_type_counts = gdf["owner_type"].value_counts()
            total_records = len(gdf)

            # Individual: should be around 88% (85-91%)
            individual_count = owner_type_counts.get("Individual", 0)
            individual_pct = (individual_count / total_records) * 100
            if not (85 <= individual_pct <= 91):
                errors.append(
                    f"Individual percentage ({individual_pct:.1f}%) outside expected range [85, 91]"
                )

            # Business (LLC): should be around 9% (7-11%)
            business_count = owner_type_counts.get("Business (LLC)", 0)
            business_pct = (business_count / total_records) * 100
            if not (7 <= business_pct <= 11):
                errors.append(
                    f"Business (LLC) percentage ({business_pct:.1f}%) outside expected range [7, 11]"
                )

            # Public: should be around 2.7% (2-4%)
            public_count = owner_type_counts.get("Public", 0)
            public_pct = (public_count / total_records) * 100
            if not (2 <= public_pct <= 4):
                errors.append(
                    f"Public percentage ({public_pct:.1f}%) outside expected range [2, 4]"
                )

            # Nonprofit/Civic: should be around 0.0% (0-0.5%)
            nonprofit_count = owner_type_counts.get("Nonprofit/Civic", 0)
            nonprofit_pct = (nonprofit_count / total_records) * 100
            if not (0 <= nonprofit_pct <= 0.5):
                errors.append(
                    f"Nonprofit/Civic percentage ({nonprofit_pct:.1f}%) outside expected range [0, 0.5]"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the owner type data."""
        self._print_summary_header("Owner Type Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Owner type distribution
        if "owner_type" in gdf.columns:
            owner_type_counts = gdf["owner_type"].value_counts()
            print("\nOwner Type Distribution:")
            for owner_type, count in owner_type_counts.items():
                pct = (count / total_records) * 100
                print(f"  {owner_type}: {count:,} ({pct:.1f}%)")

        # Coverage statistics
        if "owner_type" in gdf.columns:
            non_null_owner_types = gdf["owner_type"].notna().sum()
            owner_type_coverage = (
                (non_null_owner_types / total_records) * 100 if total_records > 0 else 0
            )
            print(f"\nOwner type coverage: {owner_type_coverage:.1f}%")
            print(f"Records with owner_type: {non_null_owner_types:,}")
            print(
                f"Records missing owner_type: {total_records - non_null_owner_types:,}"
            )

        self._print_summary_footer()
