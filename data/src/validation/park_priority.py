import geopandas as gpd
import pandera.pandas as pa

from .base import BaseValidator

# Define the Park Priority DataFrame Schema
ParkPrioritySchema = pa.DataFrameSchema(
    {
        # Core identifier - must be unique string with no NAs
        "opa_id": pa.Column(
            str, unique=True, nullable=False, description="OPA property identifier"
        ),
        # Park priority score - must be float, can be nullable, range 1.0-5.0
        "park_priority": pa.Column(
            float,
            nullable=True,
            checks=[pa.Check.in_range(1.0, 5.0, include_min=True, include_max=True)],
            description="Park priority score from TPL analysis (1.0-5.0)",
        ),
        # Geometry field - using Pandera's GeoPandas integration
        "geometry": pa.Column(
            "geometry", nullable=False, description="Property geometry"
        ),
    },
    strict=False,
    coerce=True,
)


class ParkPriorityOutputValidator(BaseValidator):
    """Validator for park priority service output with comprehensive statistical validation."""

    schema = ParkPrioritySchema
    min_stats_threshold = (
        100  # Only run statistical validation for datasets with >= 100 rows
    )

    def _row_level_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Row-level validation that works with any dataset size."""

        # Call parent class method to get empty dataframe check
        super()._row_level_validation(gdf, errors)

        # Check for required columns using helper method
        required_columns = ["park_priority", "opa_id"]
        self._validate_required_columns(gdf, required_columns, errors)

        # Validate park_priority column
        if "park_priority" in gdf.columns:
            # Check for non-numeric values (excluding nulls)
            non_null_priority = gdf["park_priority"].dropna()
            non_numeric_priority = (
                ~non_null_priority.apply(lambda x: isinstance(x, (int, float)))
            ).sum()
            if non_numeric_priority > 0:
                errors.append(
                    f"Found {non_numeric_priority} non-numeric values in 'park_priority' column"
                )

            # Check for values outside expected range (1.0 to 5.0) - excluding nulls
            out_of_range = ((non_null_priority < 1.0) | (non_null_priority > 5.0)).sum()
            if out_of_range > 0:
                errors.append(
                    f"Found {out_of_range} values outside expected range [1.0, 5.0] in 'park_priority' column"
                )

    def _statistical_validation(self, gdf: gpd.GeoDataFrame, errors: list):
        """Statistical validation that requires larger datasets."""

        # Skip statistical validation for small datasets
        if len(gdf) < self.min_stats_threshold:
            return

        # Park priority statistical validation
        if "park_priority" in gdf.columns:
            priority_stats = gdf["park_priority"].describe()

            # Check non-null percentage (should be at least 95%)
            non_null_percentage = (gdf["park_priority"].notna().sum() / len(gdf)) * 100
            if non_null_percentage < 95.0:
                errors.append(
                    f"Park priority non-null percentage ({non_null_percentage:.2f}%) below expected minimum (95.0%)"
                )

            # Check minimum value (should be around 1.50)
            min_priority = priority_stats["min"]
            if not (1.4 <= min_priority <= 1.6):
                errors.append(
                    f"Park priority minimum ({min_priority:.2f}) outside expected range [1.4, 1.6]"
                )

            # Check maximum value (should be around 5.00)
            max_priority = priority_stats["max"]
            if not (4.9 <= max_priority <= 5.1):
                errors.append(
                    f"Park priority maximum ({max_priority:.2f}) outside expected range [4.9, 5.1]"
                )

            # Check mean value (should be around 4.22)
            mean_priority = priority_stats["mean"]
            if not (4.0 <= mean_priority <= 4.5):
                errors.append(
                    f"Park priority mean ({mean_priority:.2f}) outside expected range [4.0, 4.5]"
                )

    def _print_statistical_summary(self, gdf: gpd.GeoDataFrame):
        """Print statistical summary of the park priority data."""
        self._print_summary_header("Park Priority Statistical Summary", gdf)

        # Park priority statistics
        if "park_priority" in gdf.columns:
            priority_stats = gdf["park_priority"].describe()
            print("\nPark Priority Statistics:")
            print(f"  Count: {priority_stats['count']:,.0f}")
            print(f"  Mean: {priority_stats['mean']:.2f}")
            print(f"  Std: {priority_stats['std']:.2f}")
            print(f"  Min: {priority_stats['min']:.2f}")
            print(f"  Q1: {priority_stats['25%']:.2f}")
            print(f"  Q2: {priority_stats['50%']:.2f}")
            print(f"  Q3: {priority_stats['75%']:.2f}")
            print(f"  Max: {priority_stats['max']:.2f}")

            # Non-null percentage
            non_null_percentage = (gdf["park_priority"].notna().sum() / len(gdf)) * 100
            print(f"\nNon-null percentage: {non_null_percentage:.2f}%")

            # Value distribution
            print("\nValue Distribution:")
            value_counts = gdf["park_priority"].value_counts().sort_index()
            for value, count in value_counts.items():
                pct = (count / len(gdf)) * 100
                print(f"  {value:.1f}: {count:,} ({pct:.1f}%)")

        self._print_summary_footer()
