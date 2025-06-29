import geopandas as gpd
import pandera.pandas as pa
from pandera import Check

from .base import BaseValidator


class PriorityLevelInputValidator(BaseValidator):
    """Validator for priority level service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


# Consolidated schema with all validation built-in
PriorityLevelSchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Priority level field with comprehensive validation
        "priority_level": pa.Column(
            object,  # Mixed string/NA due to "NA" fill
            nullable=True,
            checks=[
                Check(
                    lambda s: s.dropna()
                    .apply(lambda x: str(x).lower() in ["high", "medium", "low", "na"])
                    .all(),
                    error="priority_level contains invalid values (must be 'High', 'Medium', 'Low', or 'NA')",
                ),
            ],
            description="Priority level for each property (High, Medium, Low, or NA)",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
)


class PriorityLevelOutputValidator(BaseValidator):
    """Validator for priority level service output."""

    schema = PriorityLevelSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame, check_stats: bool = True):
        """Custom validation that prints actual statistics for debugging."""
        errors = []

        if "priority_level" in gdf.columns:
            # Print actual statistics for debugging
            non_null_data = gdf["priority_level"].dropna()
            if len(non_null_data) > 0:
                print("[DEBUG] priority_level validation: Actual statistics:")
                print(f"  Count: {len(non_null_data)}")
                print(f"  Unique values: {non_null_data.nunique()}")
                print(f"  Value counts: {non_null_data.value_counts().to_dict()}")

                # Check for any invalid values
                valid_values = ["high", "medium", "low", "na"]
                invalid_mask = non_null_data.apply(
                    lambda x: str(x).lower() not in valid_values
                )
                if invalid_mask.any():
                    print(
                        f"[DEBUG] priority_level validation: Found {invalid_mask.sum()} invalid values!"
                    )
                    print(
                        f"[DEBUG] priority_level validation: Invalid values: {non_null_data[invalid_mask].tolist()}"
                    )

                # Check data types
                print(
                    f"[DEBUG] priority_level validation: Data types: {non_null_data.apply(type).value_counts()}"
                )
            else:
                print("[DEBUG] priority_level validation: No non-null values found")

        self.errors.extend(errors)

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print comprehensive statistical summary of the priority level data."""
        self._print_summary_header("Priority Level Statistical Summary", gdf)

        # Total record count
        total_records = len(gdf)
        print(f"\nTotal properties: {total_records:,}")

        # Coverage statistics for priority_level column
        if "priority_level" in gdf.columns:
            non_null_count = gdf["priority_level"].notna().sum()
            coverage_pct = (
                (non_null_count / total_records) * 100 if total_records > 0 else 0
            )
            print(
                f"\npriority_level coverage: {non_null_count:,} ({coverage_pct:.1f}%)"
            )

            # Value distribution for non-null values
            non_null_data = gdf["priority_level"].dropna()
            if len(non_null_data) > 0:
                print("\npriority_level distribution:")
                value_counts = non_null_data.value_counts().sort_index()
                for value, count in value_counts.items():
                    pct = (count / len(non_null_data)) * 100
                    print(f"  {value}: {count:,} ({pct:.1f}%)")

                # Check for case sensitivity issues
                print("\npriority_level case analysis:")
                case_counts = non_null_data.apply(
                    lambda x: str(x).lower()
                ).value_counts()
                for value, count in case_counts.items():
                    pct = (count / len(non_null_data)) * 100
                    print(f"  {value} (case-insensitive): {count:,} ({pct:.1f}%)")
            else:
                print("\npriority_level: No valid data found (all values are null)")

        self._print_summary_footer()
