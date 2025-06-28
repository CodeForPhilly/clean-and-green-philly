import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Consolidated schema with all validation built-in
TacticalUrbanismSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Tactical urbanism field with comprehensive validation
        "tactical_urbanism": pa.Column(
            bool,  # Boolean type - the data utility always creates boolean values
            nullable=False,  # No nulls since data utility always creates True/False
            description="Indicates whether each property qualifies for tactical urbanism (True or False)",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class TacticalUrbanismOutputValidator(BaseValidator):
    """Validator for tactical urbanism service output."""

    schema = TacticalUrbanismSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Custom validation for tactical urbanism data."""
        errors = []

        if "tactical_urbanism" in gdf.columns:
            # Print actual statistics for debugging
            non_null_data = gdf["tactical_urbanism"].dropna()
            if len(non_null_data) > 0:
                print("[DEBUG] tactical_urbanism validation: Actual statistics:")
                print(f"  Count: {len(non_null_data)}")
                print(f"  True values: {non_null_data.sum()}")
                print(f"  False values: {(~non_null_data).sum()}")
                print(f"  Null values: {gdf['tactical_urbanism'].isna().sum()}")
                print(f"  Sample values: {non_null_data.head(10).tolist()}")

                # Check data types
                print(
                    f"[DEBUG] tactical_urbanism validation: Data types: {non_null_data.apply(type).value_counts()}"
                )

                # Check for any non-boolean values
                bool_mask = non_null_data.apply(lambda x: isinstance(x, bool))
                if not bool_mask.all():
                    print(
                        f"[DEBUG] tactical_urbanism validation: Found {(~bool_mask).sum()} non-boolean values!"
                    )
                    print(
                        f"[DEBUG] tactical_urbanism validation: Non-boolean values: {non_null_data[~bool_mask].tolist()}"
                    )
            else:
                print("[DEBUG] tactical_urbanism validation: No non-null values found")

        self.errors.extend(errors)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the tactical urbanism data."""
        self._print_summary_header("Tactical Urbanism Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for tactical_urbanism column
        if "tactical_urbanism" in gdf.columns:
            non_null_count = gdf["tactical_urbanism"].notna().sum()
            coverage_pct = (
                (non_null_count / total_records) * 100 if total_records > 0 else 0
            )
            print(
                f"\ntactical_urbanism coverage: {non_null_count:,} ({coverage_pct:.1f}%)"
            )

            # Statistical summary for non-null values
            non_null_data = gdf["tactical_urbanism"].dropna()
            if len(non_null_data) > 0:
                true_count = non_null_data.sum()
                false_count = (~non_null_data).sum()
                true_pct = (true_count / len(non_null_data)) * 100
                false_pct = (false_count / len(non_null_data)) * 100

                print("\ntactical_urbanism statistics (non-null values):")
                print(f"  True values: {true_count:,} ({true_pct:.1f}%)")
                print(f"  False values: {false_count:,} ({false_pct:.1f}%)")
                print(f"  Null values: {gdf['tactical_urbanism'].isna().sum():,}")

                # Distribution analysis
                print("\ntactical_urbanism distribution:")
                value_counts = non_null_data.value_counts().sort_index()
                for value, count in value_counts.items():
                    pct = (count / len(non_null_data)) * 100
                    print(f"  {value}: {count:,} ({pct:.1f}%)")
            else:
                print("\ntactical_urbanism: No valid data found (all values are null)")

        self._print_summary_footer()
