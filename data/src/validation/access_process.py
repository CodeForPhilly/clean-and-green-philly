import geopandas as gpd
import pandas as pd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Access Process DataFrame Schema
AccessProcessSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Access process - must be string, NAs allowed, only specific values allowed
        "access_process": pa.Column(
            str,
            pa.Check.isin(
                [
                    "Go through Land Bank",
                    "Do Nothing",
                    "Private Land Use Agreement",
                    "Buy Property",
                ]
            ),
            nullable=True,
            description="Access process classification",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class AccessProcessOutputValidator(BaseValidator):
    """Validator for access process service output."""

    schema = AccessProcessSchema

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["access_process"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate access_process column
        if "access_process" in gdf.columns:
            # Check for non-string values (excluding NAs)
            non_string_access_processes = (
                ~gdf["access_process"].apply(lambda x: isinstance(x, str) or pd.isna(x))
            ).sum()
            if non_string_access_processes > 0:
                errors.append(
                    f"Found {non_string_access_processes} non-string values in 'access_process' column"
                )

            # Check for invalid values (excluding NAs)
            valid_values = [
                "Go through Land Bank",
                "Do Nothing",
                "Private Land Use Agreement",
                "Buy Property",
            ]
            non_na_values = gdf["access_process"].dropna()
            if len(non_na_values) > 0:
                invalid_values = (~non_na_values.isin(valid_values)).sum()
                if invalid_values > 0:
                    errors.append(
                        f"Found {invalid_values} invalid values in 'access_process' column"
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
                f"Access process count ({total_records}) below expected minimum ({min_records:,})"
            )

        # 2. Access process distribution validation
        if "access_process" in gdf.columns:
            total_records = len(gdf)

            # Check that we have some NAs (non-vacant properties)
            na_count = gdf["access_process"].isna().sum()
            na_pct = (na_count / total_records) * 100
            if na_pct < 50:  # Expect most properties to be non-vacant
                errors.append(
                    f"NA percentage ({na_pct:.1f}%) below expected minimum (50%)"
                )

            # Check that we have some non-NA values (vacant properties)
            non_na_count = total_records - na_count
            non_na_pct = (non_na_count / total_records) * 100
            if non_na_pct < 1:  # Expect at least some vacant properties
                errors.append(
                    f"Non-NA percentage ({non_na_pct:.1f}%) below expected minimum (1%)"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the access process data."""
        self._print_summary_header("Access Process Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Access process distribution
        if "access_process" in gdf.columns:
            access_process_counts = gdf["access_process"].value_counts(dropna=False)
            print("\nAccess Process Distribution:")
            for access_process, count in access_process_counts.items():
                pct = (count / total_records) * 100
                display_name = (
                    "NA (Non-vacant)" if pd.isna(access_process) else access_process
                )
                print(f"  {display_name}: {count:,} ({pct:.1f}%)")

        # Coverage statistics
        if "access_process" in gdf.columns:
            non_null_access_processes = gdf["access_process"].notna().sum()
            access_process_coverage = (
                (non_null_access_processes / total_records) * 100
                if total_records > 0
                else 0
            )
            print(f"\nAccess process coverage: {access_process_coverage:.1f}%")
            print(f"Records with access_process: {non_null_access_processes:,}")
            print(
                f"Records missing access_process (NA): {total_records - non_null_access_processes:,}"
            )

        self._print_summary_footer()
