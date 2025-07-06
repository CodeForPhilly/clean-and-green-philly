import geopandas as gpd
import pandera.pandas as pa

from src.config.config import is_statistical_summaries_enabled

from .base import BaseValidator, DistributionParams


class DevProbabilityInputValidator(BaseValidator):
    """Validator for dev probability service input from census block groups."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# Distribution parameters for permit_count based on actual data
permit_counts_params = DistributionParams(
    mean=42.71, std=45.15, max_value=420.000, q1=18.000, q3=47.000
)

# Consolidated schema with all validation built-in
DevProbabilitySchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Permit count with comprehensive validation
        "permit_count": pa.Column(
            int,
            nullable=False,  # Should not have NAs (only 0s)
            checks=[
                pa.Check(
                    lambda s: s.max() <= 420.000,
                    error="permit_count maximum value exceeds 420",
                ),
                pa.Check(
                    lambda s: s.mean() >= 0.8 * 42.71 and s.mean() <= 1.2 * 42.71,
                    error="permit_count mean outside expected range [34.17, 51.25]",
                ),
                pa.Check(
                    lambda s: s.std() >= 0.8 * 45.15 and s.std() <= 1.2 * 45.15,
                    error="permit_count standard deviation outside expected range [36.12, 54.18]",
                ),
                pa.Check(
                    lambda s: s.quantile(0.25) >= 0.8 * 18.000
                    and s.quantile(0.25) <= 1.2 * 18.000,
                    error="permit_count Q1 outside expected range [14.40, 21.60]",
                ),
                pa.Check(
                    lambda s: s.quantile(0.75) >= 0.8 * 47.000
                    and s.quantile(0.75) <= 1.2 * 47.000,
                    error="permit_count Q3 outside expected range [37.60, 56.40]",
                ),
            ],
            description="Number of permits issued in the census block group",
        ),
        # Development rank with categorical validation
        "dev_rank": pa.Column(
            str,
            nullable=False,
            checks=[
                pa.Check.isin(
                    ["Low", "Medium", "High"],
                    error="dev_rank must be Low, Medium, or High",
                )
            ],
            description="Development rank of the census block group",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class DevProbabilityOutputValidator(BaseValidator):
    """Validator for dev probability service output."""

    schema = DevProbabilitySchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Custom validation that prints actual statistics for debugging."""
        # Only print statistical summary if explicitly enabled via context manager
        if is_statistical_summaries_enabled():
            self._print_statistical_summary(gdf)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the dev probability data."""
        self._print_summary_header("Development Probability Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for each column
        columns_to_check = ["permit_count", "dev_rank"]
        print("\nColumn Coverage Statistics:")
        for col in columns_to_check:
            if col in gdf.columns:
                non_null_count = gdf[col].notna().sum()
                coverage_pct = (
                    (non_null_count / total_records) * 100 if total_records > 0 else 0
                )
                print(f"  {col}: {non_null_count:,} ({coverage_pct:.1f}%)")

        # Statistical summary for permit_count
        if "permit_count" in gdf.columns:
            permit_stats = gdf["permit_count"].describe()
            print("\nPermit Count Statistics:")
            print(f"  Count: {permit_stats['count']:,.0f}")
            print(f"  Mean: {permit_stats['mean']:.3f}")
            print(f"  Std:  {permit_stats['std']:.3f}")
            print(f"  Min:  {permit_stats['min']:.3f}")
            print(f"  Max:  {permit_stats['max']:.3f}")
            print(f"  Q1:   {permit_stats['25%']:.3f}")
            print(f"  Q3:   {permit_stats['75%']:.3f}")

            # Distribution analysis
            print("\nPermit Count Distribution:")
            value_counts = gdf["permit_count"].value_counts().sort_index()
            for value, count in value_counts.head(10).items():
                pct = (count / total_records) * 100
                print(f"  {value}: {count:,} ({pct:.1f}%)")

            if len(value_counts) > 10:
                print(f"  ... and {len(value_counts) - 10} more unique values")

        # Dev rank distribution
        if "dev_rank" in gdf.columns:
            rank_counts = gdf["dev_rank"].value_counts()
            print("\nDevelopment Rank Distribution:")
            for rank, count in rank_counts.items():
                pct = (count / total_records) * 100
                print(f"  {rank}: {count:,} ({pct:.1f}%)")

        self._print_summary_footer()
