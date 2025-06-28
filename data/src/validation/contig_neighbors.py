import geopandas as gpd
import pandera.pandas as pa
from pandera import Check

from .base import BaseValidator


class ContigNeighborsInputValidator(BaseValidator):
    """Validator for contig neighbors service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# Consolidated schema with all validation built-in
ContigNeighborsSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Contiguous neighbors count with comprehensive validation
        "n_contiguous": pa.Column(
            float,  # Allow float to handle NaN values
            nullable=True,
            checks=[
                Check(
                    lambda s: s.dropna().max() <= 70,
                    error="n_contiguous maximum value exceeds 70",
                ),
                Check(
                    lambda s: s.dropna().mean() >= 0.8 * 2.566
                    and s.dropna().mean() <= 1.2 * 2.566,
                    error="n_contiguous mean outside expected range [2.05, 3.08]",
                ),
                Check(
                    lambda s: s.dropna().std() >= 3.5 and s.dropna().std() <= 7.0,
                    error="n_contiguous standard deviation outside expected range [3.5, 7.0]",
                ),
                Check(
                    lambda s: s.dropna().quantile(0.25) >= 0.8 * 0.000
                    and s.dropna().quantile(0.25) <= 1.2 * 0.000,
                    error="n_contiguous Q1 outside expected range [0.00, 0.00]",
                ),
                Check(
                    lambda s: s.dropna().quantile(0.75) >= 0.8 * 3.000
                    and s.dropna().quantile(0.75) <= 1.2 * 3.000,
                    error="n_contiguous Q3 outside expected range [2.40, 3.60]",
                ),
            ],
            description="Number of contiguous vacant neighbors for each property",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class ContigNeighborsOutputValidator(BaseValidator):
    """Validator for contig neighbors service output."""

    schema = ContigNeighborsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Custom validation that prints actual statistics for debugging."""
        errors = []

        if "n_contiguous" in gdf.columns:
            # Print actual statistics for debugging
            non_null_data = gdf["n_contiguous"].dropna()
            if len(non_null_data) > 0:
                print("[DEBUG] contig_neighbors validation: Actual statistics:")
                print(f"  Count: {len(non_null_data)}")
                print(f"  Min: {non_null_data.min()}")
                print(f"  Max: {non_null_data.max()}")
                print(f"  Mean: {non_null_data.mean()}")
                print(f"  Std: {non_null_data.std()}")
                print(f"  Q1: {non_null_data.quantile(0.25)}")
                print(f"  Q3: {non_null_data.quantile(0.75)}")
                print(f"  Sample values: {non_null_data.head(10).tolist()}")

                # Print expected ranges
                print("[DEBUG] contig_neighbors validation: Expected ranges:")
                print(f"  Max: <= 70 (actual: {non_null_data.max()})")
                print(f"  Mean: [2.05, 3.08] (actual: {non_null_data.mean():.3f})")
                print(f"  Std: [3.5, 7.0] (actual: {non_null_data.std():.3f})")
                print(
                    f"  Q1: [0.00, 0.00] (actual: {non_null_data.quantile(0.25):.3f})"
                )
                print(
                    f"  Q3: [2.40, 3.60] (actual: {non_null_data.quantile(0.75):.3f})"
                )

                # Check for boolean values
                bool_mask = non_null_data.apply(lambda x: isinstance(x, bool))
                if bool_mask.any():
                    print(
                        f"[DEBUG] contig_neighbors validation: Found {bool_mask.sum()} boolean values!"
                    )
                    print(
                        f"[DEBUG] contig_neighbors validation: Boolean values: {non_null_data[bool_mask].tolist()}"
                    )

                # Check data types
                print(
                    f"[DEBUG] contig_neighbors validation: Data types: {non_null_data.apply(type).value_counts()}"
                )

                # Check for any non-numeric values
                numeric_mask = non_null_data.apply(
                    lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
                )
                if not numeric_mask.all():
                    print(
                        f"[DEBUG] contig_neighbors validation: Found {(~numeric_mask).sum()} non-numeric values!"
                    )
                    print(
                        f"[DEBUG] contig_neighbors validation: Non-numeric values: {non_null_data[~numeric_mask].tolist()}"
                    )
            else:
                print("[DEBUG] contig_neighbors validation: No non-null values found")

        self.errors.extend(errors)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the contig neighbors data."""
        self._print_summary_header("Contiguous Neighbors Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for n_contiguous column
        if "n_contiguous" in gdf.columns:
            non_null_count = gdf["n_contiguous"].notna().sum()
            coverage_pct = (
                (non_null_count / total_records) * 100 if total_records > 0 else 0
            )
            print(f"\nn_contiguous coverage: {non_null_count:,} ({coverage_pct:.1f}%)")

            # Statistical summary for non-null values
            non_null_data = gdf["n_contiguous"].dropna()
            if len(non_null_data) > 0:
                stats = non_null_data.describe()
                print("\nn_contiguous statistics (non-null values):")
                print(f"  Mean: {stats['mean']:.3f}")
                print(f"  Std:  {stats['std']:.3f}")
                print(f"  Min:  {stats['min']:.3f}")
                print(f"  Max:  {stats['max']:.3f}")
                print(f"  Q1:   {stats['25%']:.3f}")
                print(f"  Q3:   {stats['75%']:.3f}")

                # Distribution analysis
                print("\nn_contiguous distribution:")
                value_counts = non_null_data.value_counts().sort_index()
                for value, count in value_counts.head(10).items():
                    pct = (count / len(non_null_data)) * 100
                    print(f"  {value}: {count:,} ({pct:.1f}%)")

                if len(value_counts) > 10:
                    print(f"  ... and {len(value_counts) - 10} more unique values")
            else:
                print("\nn_contiguous: No valid data found (all values are null)")

        self._print_summary_footer()
