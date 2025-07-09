import geopandas as gpd
import pandas as pd
import pandera.pandas as pa
from pandera import Check

from .base import BaseValidator


class DelinquenciesInputValidator(BaseValidator):
    """Validator for delinquencies service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        pass


# Consolidated schema with all validation built-in
DelinquenciesSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Tax delinquency fields with comprehensive validation
        "num_years_owed": pa.Column(
            "Int64",  # Service converts to Int64 with pd.to_numeric().astype("Int64")
            nullable=True,
            checks=[
                Check(
                    lambda s: s.dropna().max() <= 45,
                    error="num_years_owed maximum value exceeds 45",
                ),
            ],
            description="Number of years of tax delinquency",
        ),
        "total_due": pa.Column(
            object,  # Mixed float/string due to "NA" fill
            nullable=True,
            checks=[
                Check(
                    lambda s: pd.to_numeric(s, errors="coerce").dropna().max()
                    <= 1200000,
                    error="total_due maximum value exceeds 1.2M",
                ),
            ],
            description="Total amount owed in tax delinquency",
        ),
        "total_assessment": pa.Column(
            object,  # Mixed float/string due to "NA" fill
            nullable=True,
            checks=[
                Check(
                    lambda s: pd.to_numeric(s, errors="coerce").dropna().max()
                    <= 140000000,
                    error="total_assessment maximum value exceeds 140M",
                ),
            ],
            description="Total property assessment value",
        ),
        "is_actionable": pa.Column(
            object,
            nullable=True,  # Allow NaN values from LEFT JOIN
            description="Flag for actionable tax delinquency",
        ),
        "sheriff_sale": pa.Column(
            object,
            nullable=True,  # Allow NaN values from LEFT JOIN
            description="Indicates if the property is at risk of sheriff sale",
        ),
        "payment_agreement": pa.Column(
            object,
            nullable=True,  # Allow NaN values from LEFT JOIN
            description="Indicates if there is a payment agreement in place",
        ),
        "most_recent_year_owed": pa.Column(
            object,  # Mixed datetime/string due to "NA" fill
            nullable=True,
            description="Most recent year of tax delinquency",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class DelinquenciesOutputValidator(BaseValidator):
    """Validator for delinquencies service output."""

    schema = DelinquenciesSchema

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the delinquencies data."""
        self._print_summary_header("Delinquencies Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for each column
        columns_to_check = [
            "num_years_owed",
            "total_due",
            "total_assessment",
            "is_actionable",
            "sheriff_sale",
            "payment_agreement",
            "most_recent_year_owed",
        ]

        print("\nColumn Coverage Statistics:")
        for col in columns_to_check:
            if col in gdf.columns:
                non_null_count = gdf[col].notna().sum()
                coverage_pct = (
                    (non_null_count / total_records) * 100 if total_records > 0 else 0
                )
                print(f"  {col}: {non_null_count:,} ({coverage_pct:.1f}%)")

        # Statistical summaries for numeric columns
        numeric_columns = ["num_years_owed", "total_due", "total_assessment"]
        for col in numeric_columns:
            if col in gdf.columns:
                # Convert "NA" strings to nulls for analysis
                data = gdf[col].replace("NA", pd.NA)
                numeric_data = pd.to_numeric(data, errors="coerce")
                non_null_data = numeric_data.dropna()

                if len(non_null_data) > 0:
                    stats = non_null_data.describe()
                    print(f"\n{col} statistics (non-null values):")
                    print(f"  Mean: {stats['mean']:.2f}")
                    print(f"  Std:  {stats['std']:.2f}")
                    print(f"  Min:  {stats['min']:.2f}")
                    print(f"  Max:  {stats['max']:.2f}")
                    print(f"  Q1:   {stats['25%']:.2f}")
                    print(f"  Q3:   {stats['75%']:.2f}")
                else:
                    print(f"\n{col}: No valid numeric data found")

        # Boolean column summaries
        boolean_columns = ["is_actionable", "sheriff_sale", "payment_agreement"]
        for col in boolean_columns:
            if col in gdf.columns:
                value_counts = gdf[col].value_counts()
                print(f"\n{col} distribution:")
                for value, count in value_counts.items():
                    pct = (count / total_records) * 100
                    print(f"  {value}: {count:,} ({pct:.1f}%)")

        self._print_summary_footer()
